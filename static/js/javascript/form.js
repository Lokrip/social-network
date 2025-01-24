class Form {
    constructor(form) {
        this.form = form;
    }


    action(extraElement) {
        this.form.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(event.currentTarget);

            for (let [key, value] of formData.entries()) {
                console.log(key, value)
            }
            
            try {
                const response = await fetch(`http://127.0.0.1:8000/api/v1/create-post/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,  // Заголовок CSRF токена
                    },
                    body: formData  // Отправляем данные в формате FormData
                });
        
                const data = await response.json();
                console.log(data);
                const {status, post} = data;
                if (data && status === "redirect") {
                    window.location.href = "/";
                }
            } catch (error) {
                console.error('Error submitting form:', error);
            }
        });
    }
}

const formElement = document.querySelector('#myCreatedPostForm');
const form = new Form(formElement);

form.action('additional data');