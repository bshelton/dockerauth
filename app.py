import base64, json

from flask import Flask, jsonify, request

application = Flask(__name__)


@application.route("/")
def index():
    return "Docker Authz Plugin"

@application.route("/Plugin.Activate", methods=['POST'])
def activate():
    return jsonify({'Implements': ['authz']})


@application.route("/AuthZPlugin.AuthZReq", methods=['POST'])
def authz_request():
    print("AuthZ Request")
    response = {}

    plugin_request = json.loads(request.data)
    print (plugin_request)

    #Set the user who send the command
    user = plugin_request['RequestHeaders']['Authz-User']
    
    if 'DELETE' in plugin_request['RequestMethod']:
        if str(user) == 'root':
            response = {"Allow": True,
                        "Msg":   "Image can be deleted by root",
                        "Err":   "You are not allowed to perform this action!"}
            return jsonify(**response)
        else:
            response = {"Allow": False,
                        "Msg":   "Only root can delete an image.",
                        "Err":   "You are not allowed to perform this action!"}
            return jsonify(**response)


    if 'containers' in plugin_request['RequestUri']:
        print(plugin_request)
        encoded_docker_request = plugin_request
        #docker_request = json.loads(base64.b64decode(encoded_docker_request))
        response = {"Allow": True,
                    "Msg":   "Everyone can list containers.",
                    "Err":   "I dont know what could go wrong."}

    elif 'images' in plugin_request['RequestUri']:
        response = {"Allow": True,
                    "Msg":   "Everyone can list images.",
                    "Err":   "I dont know what could go wrong."}
    else:
        response = {"Allow": False,
                    "Msg":   "You are not allowed to perform this action!",
                    "Err":   "You are not allowed to perform this action!"}

    return jsonify(**response)

@application.route("/AuthZPlugin.AuthZRes", methods=['POST'])
def authz_response():
    print("AuthZ Response")
    response = {"Allow": True}
    return jsonify(**response)



if __name__ == "__main__":
    application.run(host='0.0.0.0')