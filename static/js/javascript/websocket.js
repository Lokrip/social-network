class WebSocketConnect {
    constructor(is_connect = false, host, route) {
        if (is_connect) {
            this.webSocket = new WebSocket(`ws://${host}/${route}`);
            this.webSocket.onopen = () => console.log("WebSocket connected!");
        } else {
            this.webSocket = null; // Handle cases where no connection is needed
        }
    }

    message(callback) {
        this.webSocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            callback(data)
        }
    }

    send(data) {
        if (this.webSocket.readyState === WebSocket.OPEN) {
            this.webSocket.send(data);
        } else {
            this.webSocket.onopen = () => {
                this.webSocket.send(data);
            };
        }
    }

}