class FriendShip {
    constructor(webSocketConnect, profile) {
        if(profile instanceof Profile) {
            this.profile = profile
        }

        if(webSocketConnect instanceof WebSocketConnect) {
            this.webSocketConnect = webSocketConnect
        }
    }
}