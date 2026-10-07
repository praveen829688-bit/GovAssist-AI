from http.server import BaseHTTPRequestHandler
import json
import os


class handler(BaseHTTPRequestHandler):

    def send_json(self, status, data):

        body = json.dumps(data).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, OPTIONS"
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )

        self.end_headers()

        self.wfile.write(body)

    def do_OPTIONS(self):

        self.send_json(
            200,
            {"status": "ok"}
        )

    def do_GET(self):

        self.send_json(
            200,
            {
                "name": "GovAssist AI",
                "status": "online",
                "message": "GovAssist AI API is running.",
                "version": "1.0"
            }
        )

    def do_POST(self):

        try:

            content_length = int(
                self.headers.get(
                    "Content-Length",
                    0
                )
            )

            raw = self.rfile.read(
                content_length
            )

            data = json.loads(
                raw.decode("utf-8")
            )

            message = data.get(
                "message",
                ""
            )

            if not message:

                self.send_json(
                    400,
                    {
                        "error": "Message is required."
                    }
                )

                return

            # Import the existing AI engine.
            try:

                from ai_engine import ask_ai

                answer = ask_ai(message)

            except Exception as exc:

                answer = (
                    "GovAssist AI received your question, "
                    "but the AI service is currently unavailable."
                )

            self.send_json(
                200,
                {
                    "success": True,
                    "message": message,
                    "answer": answer
                }
            )

        except Exception as exc:

            self.send_json(
                500,
                {
                    "success": False,
                    "error": str(exc)
                }
            )
