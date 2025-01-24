function friendInitialize(profileManager) {
    const webSocketConnectFriends = new WebSocketConnect(
        true, 
        window.location.host, 
        "ws/create-friends/"
    );
    const friendShipManager = new FriendShip(
        webSocketConnectFriends, 
        profileManager
    )
    
    return {
        webSocketConnect: webSocketConnectFriends,
        friendShipManager: friendShipManager
    }
}
function notificationInitialize(profileManager) {
    const webSocketConnectNotification = new WebSocketConnect(
        true, 
        window.location.host, 
        "ws/notification/"
    );
    const notificationManager = new Notification(
        webSocketConnectNotification, 
        profileManager
    )
    
    return {
        webSocketConnect: webSocketConnectNotification,
        notificationManager: notificationManager
    }
}
function init() {
    const profileManager = new Profile()
    try {
        const webSocketConnectChat = new WebSocketConnect(
            true, 
            window.location.host, 
            `ws/chat/room/${chatUuid}/`
        );

        const chatForm = document.querySelector('#chat-form')
        const chatInputBody = document.querySelector("#chat-input-body")
        console.log(chatForm, chatInputBody)
        
        chatForm.addEventListener("submit", (event) => {
            event.preventDefault()
            webSocketConnectChat.send(JSON.stringify({
                body: chatInputBody.value
            }))
        })

        webSocketConnectChat.message((data) => {
            console.log(data)
        })

    } catch(error) {}
    const {
        webSocketConnect: webSocketConnectFriends, 
        friendShipManager
    } = friendInitialize(profileManager)

    const {
        webSocketConnect: webSocketConnectNotification, 
        notificationManager
    } = notificationInitialize(profileManager)


}

window.addEventListener("DOMContentLoaded", init)
