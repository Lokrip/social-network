class StoryFetching extends Fetching {
    constructor() {
        super("http://127.0.0.1:8000/api/v1/")
    }

    async fetchStory(pk) {
        return await this.fetchData(`story/${pk}/`)
    }
}

class Story {
    constructor(listContainerStory) {
        if(listContainerStory instanceof HTMLElement) {
            this.listContainerStory = listContainerStory
        }
    }
    
    storyViewer(callback) {
        const delegationEvent = (event) => {
            const Modalstory = document.querySelector("#Modalstory")
            const target = event.target;
            if(target.closest("[data-story]")) {
                callback(target, Modalstory)
            }
        }
        this.listContainerStory.addEventListener(
            "click", 
            delegationEvent
        )
    }
}


window.addEventListener("DOMContentLoaded", () => {
    const ListStory = document.querySelector("#list-item-story")
    const store = new Story(ListStory);
    const storyFetching = new StoryFetching()
    store.storyViewer(async (target, modalstory) => {
        const listImageStory = modalstory.querySelector("#list-story-image")
        
        const story_id = target.getAttribute("data-story-id")
        const data = await storyFetching.fetchStory(story_id)
        const html = `<div class="item"><img src="${data.image}" alt="image"></div>`
        listImageStory.innerHtml = ""
        listImageStory.insertAdjacentHTML("beforeend", html)
        console.log(data, listImageStory, html)
    })
})