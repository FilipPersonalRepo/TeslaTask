import json
import yaml
import shutil
import os

class VarsetGenerator:
    def __init__(self, input:str):
        with open(input, 'r') as file:
            self.configs = yaml.safe_load(file)

        self.params = self.configs['parameters']
        self.env = self.params['env']
        self.source_folder = self.configs['source_folder']
        self.source_template = self.configs['source_template']
        self.cwd = os.getcwd()
        self.src_path = os.path.join(self.cwd, self.source_folder, self.source_template)
        self.dest_path = self.src_path.replace(self.source_template, self.env)
        print(f"params: {self.params}")
        print(f"env: {self.env}")
        print(f"source_folder: {self.source_folder}")
        print(f"source_template: {self.source_template}")
        print(f"cwd: {self.cwd}")
        print(f"src_path: {self.src_path}")
        print(f"dest_path: {self.dest_path}")

    def copy_folder(self):
        print("START: Copying template folder structure !")
        try:
            shutil.copytree(self.src_path, self.dest_path)
            print("END: Copying template folder structure !")
        except Exception as e:
            print("Error is:\n", e)

    def read_df(self, path):
        print(f"START: Reading {path} !")
        with open(path, 'r') as file:
            data = json.load(file)
        return data

    def replace_placeholders(self, data, params):
        if isinstance(data, str):
            for key, value in params.items():
                data = data.replace(f"{{{{{key}}}}}", value)
            return data
        elif isinstance(data, dict):
            return {key: self.replace_placeholders(value, params) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.replace_placeholders(item, params) for item in data]
        return data

    def write_df(self, df, path):
        print(f"START: Writing {path} !")
        with open(path, 'w') as json_file:
            json.dump(df, json_file, indent=4)
            print(f"Writing to {path} DONE")

    def list_files(self, dest_path):
        for root, dirs, files in os.walk(dest_path):
            for filename in files:
                full_path = os.path.join(root, filename)
                data = self.read_df(full_path)
                updated_json_data = self.replace_placeholders(data, self.params)
                self.write_df(updated_json_data, full_path) 

    def run(self):
        self.copy_folder()
        self.list_files(self.dest_path)
      

if __name__ == "__main__":
    cl = VarsetGenerator('Configs/input.yml')
    cl.run()
