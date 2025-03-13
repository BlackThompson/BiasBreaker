from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from multiagents import setup_conversation, run_conversation, get_agent_info
import logging
import json
import queue
import threading

app = Flask(__name__)
CORS(app)

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建一个消息队列
message_queue = queue.Queue()


def generate_messages():
    while True:
        message = message_queue.get()  # 这会阻塞直到有新消息
        if message is None:  # 结束信号
            break
        yield f"data: {json.dumps(message)}\n\n"


@app.route("/api/start-conversation", methods=["POST"])
def start_conversation():
    try:
        # 清空之前的消息队列
        while not message_queue.empty():
            message_queue.get()

        def run_agents():
            agents = setup_conversation()
            run_conversation(agents, message_queue)
            # 发送结束信号
            message_queue.put(None)

        # 在新线程中运行对话
        thread = threading.Thread(target=run_agents)
        thread.start()

        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Error in conversation: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/messages")
def messages():
    return Response(
        generate_messages(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        },
    )


if __name__ == "__main__":
    logger.info("Starting Flask server...")
    app.run(debug=True, port=5000, threaded=True)
