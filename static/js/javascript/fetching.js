class Fetching {
    constructor(baseUrl) {
        //проверяем если создаеться экземпляр класса то мы делаем ошибку
        //таким оброзом мы класс делаем обстрактным
        if (new.target === Fetching) {
            throw new Error("Cannot instantiate abstract class Fetching directly");
        }
        this.baseUrl = baseUrl;
    }

    async fetchData(endpoint, {
        is_pagination = false,
        pagination_page = 1,
    } = {}) {
        try {
            const response = (
                is_pagination
                ? await fetch(`${this.baseUrl}${endpoint}?page=${pagination_page}`)
                : await fetch(`${this.baseUrl}${endpoint}`)
            );

            console.log(response)

            if(!response.ok) {
                throw new Error(`Response Status: ${response.status}`)
            }
            const data = await response.json()
            return data
        } catch(error) {
            console.error(error.message)
            throw error;
        }
    }
}
