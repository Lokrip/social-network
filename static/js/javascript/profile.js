class ProfileFetching extends Fetching {
    constructor() {
        super("http://127.0.0.1:8000/account/api/v1/")
    }

    async fetchUser() {
        return await this.fetchData('user-detail/')
    }
}

class Profile extends ProfileFetching {
    constructor() {
        super();
        
        const profileRecipient = document.querySelector('[data-username-recipient]')
        const usernameSender = document.querySelector("[data-username-sender]")
        const usernameRecipient = document.querySelector("[data-username-recipient]")

        if(profileRecipient || usernameSender || usernameRecipient) {
            this.usernameSender = usernameSender
            this.usernameRecipient = usernameRecipient || profileRecipient
        }
    }
    
    getUsernameSender() {return this.usernameSender.getAttribute("data-username-sender")}
    getUsernameRecipient() {return this.usernameRecipient.getAttribute("data-username-recipient")}
}
