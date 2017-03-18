from __future__ import print_function
import sys, json
from flask import Flask
from github import Github
from collections import OrderedDict
app = Flask(__name__)

@app.route("/v1/<variable>")
def hello(variable):
    try:
        g = Github()
        url = str(sys.argv[1])
        user_n = url.split("github.com/")[1]
        user_name = user_n.split("/")[0]
        repo_name = user_n.split("/")[1]
        user = g.get_user(user_name)
        #repo_name should be "cmpe273-assignment1"
        repository = user.get_repo(repo_name)
        file_name = variable.split(".")[0]
        file_fname = file_name + ".yml"
        file_content = repository.get_contents(file_fname).content
        content = file_content.decode("base64")
        if variable.endswith(".yml"):
            return content
        elif variable.endswith(".json"):
            content_a = content.split("\n")
            final_content = "{"
            i = 0
            for each in content_a:
                if each.isspace() or not each:
                    continue
                if i > 0:
                    final_content += ","
                temp_a = each.split(":")
                final_content += '"'+temp_a[0]+'":'+temp_a[1]
                i += 1
            final_content += "}"
            debug_text = "success: " + final_content
            #print(debug_text, file=sys.stderr)
            s_content = json.loads(final_content, object_pairs_hook=OrderedDict)
            return json.dumps(s_content, sort_keys=False, indent=2, separators=(',', ': '))
        else:
            return "The rest api ends with a data format, which is not supported."
    except:
        debug_text = "FAIL"
        print(debug_text, file=sys.stderr)
        return "Something wrong with command line parameter or api call"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
