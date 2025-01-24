class DOMElementManager {
    constructor(element) {
        if (!element) {
            throw new Error('A valid DOM element is required');
        }
        this.element = element;
    }
}

class StylesManager extends DOMElementManager {
    addClass(className) {
        if (className) {
            this.element.classList.add(className);
        }
        return this;
    }

    removeClass(className) {
        if (className) {
            this.element.classList.remove(className);
        }
        return this;
    }

    toggleClass(className) {
        if (className) {
            this.element.classList.toggle(className);
        }
        return this;
    }

    containsClass(className) {
        return className ? this.element.classList.contains(className) : false;
    }
}

class AttributeManager extends DOMElementManager {
    setAttribute(attribute, value) {
        if (attribute) {
            this.element.setAttribute(attribute, value);
        }
        return this;
    }

    getAttribute(attribute) {
        return attribute ? this.element.getAttribute(attribute) : null;
    }
}

class ElementFactory {
    static createElement(tagName) {
        if (typeof tagName !== 'string' || !tagName.trim()) {
            throw new Error('A valid tag name must be provided');
        }
        return document.createElement(tagName);
    }
}