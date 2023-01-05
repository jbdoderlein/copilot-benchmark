"""Copilot implementation"""
import json
import os
import copy
import subprocess

from .doc import Document

class Agent:
    """Control the Node Copilot Agent"""
    def __init__(self, agent_path : str = "dist/agent.js"):
        self.agent_path = os.path.abspath(agent_path)
        self.job = self.create_job()
        self.stdin = self.job.stdin
        self.stdout = self.job.stdout
        self.id = 0

    def create_job(self) -> subprocess.Popen:
        """Create a subprocess with the agent"""
        return subprocess.Popen(
            ["node", self.agent_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    def send(self, data : dict) -> None:
        """Send data to the agent"""
        data.update({"jsonrpc": "2.0"})
        data = json.dumps(data)
        request = f"Content-Length: {len(data)}\r\n\r\n{data}"
        self.stdin.write(request.encode())
        self.stdin.flush()

    def agent_request(self, method : str, params : dict) -> None:
        """Send a request to the agent"""
        self.id += 1
        request = {
            "method": method,
            "params": params,
            "id": self.id
        }
        self.send(request)


    def get_output(self) -> dict:
        """Get the output from the agent"""
        content_length = self.stdout.readline().decode().strip()
        self.stdout.readline() # \r\n line
        output = self.stdout.read(int(content_length.replace('\r\n','')[16:])).decode()
        res = json.loads(output)
        return res


class Copilot:
    """Copilot API"""
    def __init__(self, agent_path : str = "dist/agent.js"):
        self.agent = Agent(agent_path)
        self.agent.get_output()
        self.set_editor_info()

    def set_editor_info(self):
        """Set the editor info"""
        self.agent.send({
            "method": "initialize",
            "workspace": {"workspaceFolders": True},
            "id": self.agent.id,
            "params": {"capabilities": {}}
        })
        self.agent.id += 1
        self.agent.agent_request("setEditorInfo", {
            "editorPluginInfo": {
                "version": "1.8.0",
                "name": "copilot.vim"
            },
            "editorInfo": {
                "version": "0.8.1",
                "name": "Neovim"
            }
        })
        # Clear stdin
        self.agent.get_output()
        self.agent.get_output()
        self.agent.get_output()

    def get_panel_completion(self, doc : Document) -> list[Document]:
        """Get the panel completion, a list of 10 completions with score"""
        self.agent.agent_request("getPanelCompletions", {
            'doc':doc.to_dict(),
            "panelId": "copilot:///1"
        })
        solution = []
        while (res:=self.agent.get_output()) is not None:
            if 'method' in res:
                if res['method'] == 'PanelSolution':
                    ndoc = copy.deepcopy(doc)
                    ndoc.add_content(res['params']['displayText'], keep_cursor=False)
                    solution.append((res['params']['score'], ndoc))
                elif res['method'] == 'PanelSolutionsDone':
                    return solution
        solution.sort(reverse=True)
        return solution

    def get_completion(self, doc : Document, max_steps = 1) -> Document:
        """Get the completion of current cursor """
        step = 0
        while step < max_steps:
            step += 1
            self.agent.agent_request("getCompletions", {'doc': doc.to_dict()})
            partial_solution = False
            while not partial_solution:
                res = self.agent.get_output()
                if 'id' in res and 'result' in res:
                    if 'completions' in res['result']:
                        if len(res['result']['completions']) == 0:
                            print("Copilot no completion")
                            doc.add_content("", keep_cursor=False)
                            return doc
                        doc.add_content(res['result']['completions'][0]['displayText'], keep_cursor=True)
                        partial_solution = True
        doc.add_content("", keep_cursor=False)
        return doc

    def get_all_completion(self, doc : Document, max_steps = 1) -> Document:
        """Get all the completion"""
        for _ in range(len(doc.position)):
            doc = self.get_completion(doc, max_steps)
        return doc

    def get_panel_completions(self, doc : Document) -> list[list[(float, Document)]]:
        res = [[(1,doc)]]
        for i in range(len(doc.position)):
            print(f"Step {i}/{len(doc.position)}")
            res.append(self.get_panel_completion(res[-1][0][1]))
        return res
