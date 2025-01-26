function createWebSocketConnection(path) {
    return new WebSocketConnect(true, window.location.host, path);
}

function chatInitialize(profileManager) {
    const chatForm = document.querySelector('#chat-form')
    const chatInputBody = document.querySelector("#chat-input-body")

    const chatListMessagesContainer = document.querySelector("#chat-list-messages-container")

    let webSocketConnectChat = null;


    try {
        webSocketConnectChat = createWebSocketConnection(`ws/chat/room/${chatUuid}/`);
    } catch(error) {
        console.warn("chatUuid not found")
    }

    const chatManager = new Chat(webSocketConnectChat, profileManager,);

    chatManager.sendingMessage(chatForm, chatInputBody)
    chatManager.addMessageToList(chatListMessagesContainer)

    return {
        webSocketConnect: webSocketConnectChat,
        chatManager: chatManager
    }
}
function friendInitialize(profileManager) {
    const webSocketConnectFriends = createWebSocketConnection("ws/create-friends/");
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
    const webSocketConnectNotification = createWebSocketConnection("ws/notification/");
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

    const chatConfig = chatInitialize(profileManager);
    const friendConfig = friendInitialize(profileManager);
    const notificationConfig = notificationInitialize(profileManager);


    const { webSocketConnect: webSocketConnectChat, chatManager } = chatConfig;
    const { webSocketConnect: webSocketConnectFriends, friendShipManager } = friendConfig;
    const { webSocketConnect: webSocketConnectNotification, notificationManager } = notificationConfig;
}

window.addEventListener("DOMContentLoaded", init)
