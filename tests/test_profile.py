import copy
import json
import re
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import github_data
import render_profile
import refresh


class ProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((ROOT/"data/public-repos.json").read_text(encoding="utf-8"))
        cls.config=json.loads((ROOT/"profile.json").read_text(encoding="utf-8"))

    def test_all_public_repositories_appear_and_assets_exist(self):
        outputs=render_profile.render(self.data)
        readme=outputs["readme.md"]
        for repo in self.data["repos"]:
            self.assertIn(repo["html_url"],readme)
        for asset in re.findall(r'(?:src|srcset)="(assets/[^"]+)"',readme):
            self.assertIn(asset,outputs)
            self.assertTrue((ROOT/asset).is_file())
        self.assertNotRegex(readme,r'YOUR_|count_private|vercel\.app/api|herokuapp|shields\.io|raw\.githubusercontent')

    def test_svg_is_valid_and_self_contained(self):
        for name,content in render_profile.render(self.data).items():
            if not name.endswith(".svg"):
                continue
            with self.subTest(asset=name):
                root=ET.fromstring(content)
                self.assertEqual(root.tag,"{http://www.w3.org/2000/svg}svg")
                for node in root.iter():
                    self.assertNotIn(node.tag.rsplit("}",1)[-1],("script","foreignObject","image"))
                    self.assertFalse(any(k.lower().startswith("on") for k in node.attrib))
                self.assertIn("prefers-reduced-motion",content)
                self.assertIn('<title id="title">',content)

    def test_new_repo_appears_without_manual_configuration(self):
        data=copy.deepcopy(self.data)
        new=copy.deepcopy(data["repos"][0])
        new.update(name="fresh-public-project",html_url="https://github.com/sankalpjoe/fresh-public-project",
                   description='A | B <script>test</script>\nnext line',archived=False)
        data["repos"].append(new)
        readme=render_profile.markdown(data,self.config)
        self.assertIn(new["html_url"],readme)
        self.assertIn('A &#124; B &lt;script&gt;test&lt;/script&gt; next line',readme)
        self.assertNotIn('<script>',readme)

    def test_absent_or_empty_feature_is_not_linked(self):
        data=copy.deepcopy(self.data)
        data["repos"]=[r for r in data["repos"] if r["name"]!="dashboard"]
        for repo in data["repos"]:
            if repo["name"]=="doc-toolkit": repo["size"]=0
        outputs=render_profile.render(data)
        readme=outputs["readme.md"]
        self.assertNotIn("https://github.com/sankalpjoe/dashboard",readme)
        self.assertNotIn("assets/project-doc-toolkit.svg",readme)
        self.assertIn("https://github.com/sankalpjoe/doc-toolkit",readme)

    def test_language_totals_exclude_archives_forks_and_profile(self):
        base={"name":"project","fork":False,"archived":False,"languages":{"Python":100}}
        data={"repos":[base,dict(base,name="sankalpjoe"),dict(base,fork=True),dict(base,archived=True)]}
        self.assertEqual(render_profile.language_totals(data),[("Python",100)])
        self.assertIn("No language data",render_profile.spectrum({"repos":[]}))

    def test_existing_states(self):
        for repo in self.data["repos"]:
            if repo["archived"]: self.assertEqual(render_profile.status(repo),"Archived")
            elif repo["name"]=="sankalpjoe": self.assertEqual(render_profile.status(repo),"Profile")
            elif not repo["size"]: self.assertEqual(render_profile.status(repo),"Empty")

    def test_invalid_snapshot_is_rejected(self):
        data=copy.deepcopy(self.data)
        data["repos"][0]["html_url"]="https://example.com/wrong-owner"
        with self.assertRaises(ValueError): refresh.validate(data)
        data=copy.deepcopy(self.data)
        data["repos"][0]["name"]="../../outside"
        with self.assertRaises(ValueError): refresh.validate(data)
        data=copy.deepcopy(self.data)
        data["repos"].append(data["repos"][0])
        with self.assertRaises(ValueError): refresh.validate(data)

    def test_public_api_pagination_and_private_filter(self):
        first=[{"name":f"repo-{i}","owner":{"login":"sankalpjoe"},"private":False} for i in range(100)]
        second=[{"name":"private-one","owner":{"login":"sankalpjoe"},"private":True},
                {"name":"last-public","owner":{"login":"sankalpjoe"},"private":False}]
        def api(path):
            if path=="/users/sankalpjoe": return {"followers":1}
            if path.endswith("&page=1"): return first
            if path.endswith("&page=2"): return second
            if path.endswith("/languages"): return {"Python":10}
            raise AssertionError(path)
        with patch.object(github_data,"request",side_effect=api):
            data=github_data.collect()
        self.assertEqual(len(data["repos"]),101)
        self.assertIn("last-public",[r["name"] for r in data["repos"]])
        self.assertNotIn("private-one",[r["name"] for r in data["repos"]])

    def test_failed_fetch_leaves_existing_snapshot_and_readme_untouched(self):
        paths=[ROOT/"data/public-repos.json",ROOT/"readme.md"]
        before=[p.read_bytes() for p in paths]
        with patch.object(sys,"argv",["refresh.py"]), patch.object(refresh,"collect",side_effect=RuntimeError("API unavailable")):
            with self.assertRaises(RuntimeError): refresh.main()
        self.assertEqual(before,[p.read_bytes() for p in paths])

    def test_api_failure_is_not_converted_into_empty_data(self):
        with patch.object(github_data,"urlopen",side_effect=HTTPError("url",403,"rate limit",{},None)):
            with self.assertRaises(HTTPError): github_data.request("/users/sankalpjoe")


if __name__=="__main__":
    unittest.main()
