class EventManager {
    attachEvent(element, eventType, handler) {
        if (!element || !eventType || typeof handler !== 'function') {
            throw new Error('Invalid arguments for attaching event');
        }
        element.addEventListener(eventType, handler)
    }
}

class StoryEvent extends EventManager {}
