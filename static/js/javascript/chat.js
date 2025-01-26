class PostFetching extends Fetching {
    constructor() {
        super("")
    }

    async fetchUser(pagination_page = 1) {

    }
}

class Chat {
    constructor(webSocketConnect, profile) {
        if(profile instanceof Profile) {
            this.profile = profile
        }

        if(webSocketConnect instanceof WebSocketConnect && webSocketConnect) {
            this.webSocketConnect = webSocketConnect
        }
    }

    sendingMessage(chatForm, chatInput) {
        if(!this.webSocketConnect && !chatForm && !chatInput) {
            console.warn("Not Found webSocketConnect, chatForm, chatInput")
            return;
        }

        chatForm.addEventListener("submit", (event) => {
            event.preventDefault()

            this.webSocketConnect.send(JSON.stringify({
                body: chatInput.value
            }))
        })
    }

    addMessageToList(listContainer) {
        if(!listContainer) {return;}

        this.webSocketConnect.message((data) => {
            console.log(data)
        })
    }
}
