class PostFetching extends Fetching {
    constructor() {
        super("http://127.0.0.1:8000/api/v1/")
    }

    async fetchPosts(pagination_page = 1) {
        const {results} = await this.fetchData('posts/', {
            is_pagination: true,
            pagination_page: pagination_page
        })
        return results
    }
}

class PostCardGenerator {
    getCard(data) {
        const html = `<div class="card w-100 shadow-xss rounded-xxl border-0 p-4 mb-0 mb-3">
        <div class="card-body p-0 d-flex">
            <figure class="avatar me-3"><img src="${data.user.image}" alt="image" class="shadow-sm rounded-circle w45"></figure>
            <h4 class="fw-700 text-grey-900 font-xssss mt-1">${data.user.username} <span class="d-block font-xssss fw-500 mt-1 lh-3 text-grey-500">2 hour ago</span></h4>
            <a href="#" class="ms-auto"><i class="ti-more-alt text-grey-900 btn-round-md bg-greylight font-xss"></i></a>
        </div>
        <div class="card-body p-0 me-lg-5">
            <p class="fw-500 text-grey-500 lh-26 font-xssss w-100 mb-2">${data.content} <a href="#" class="fw-600 text-primary ms-2">See more</a></p>
        </div>
        <div class="card-body d-block p-0 mb-3">
            <div class="row ps-2 pe-2">
                <div class="col-sm-12 p-1"><a href="" data-lightbox="roadtr"><img src="${data.product_images.image}" class="rounded-3 w-100" alt="image"></a></div>
            </div>
        </div>
        <div class="card-body d-flex p-0">
            <a href="#" class="emoji-bttn d-flex align-items-center fw-600 text-grey-900 text-dark lh-26 font-xssss me-2"><i class="feather-thumbs-up text-white bg-primary-gradiant me-1 btn-round-xs font-xss"></i> <i class="feather-heart text-white bg-red-gradiant me-2 btn-round-xs font-xss"></i>2.8K Like</a>
            <div class="emoji-wrap">
                <ul class="emojis list-inline mb-0">
                    <li class="emoji list-inline-item"><i class="em em---1"></i> </li>
                    <li class="emoji list-inline-item"><i class="em em-angry"></i></li>
                    <li class="emoji list-inline-item"><i class="em em-anguished"></i> </li>
                    <li class="emoji list-inline-item"><i class="em em-astonished"></i> </li>
                    <li class="emoji list-inline-item"><i class="em em-blush"></i></li>
                    <li class="emoji list-inline-item"><i class="em em-clap"></i></li>
                    <li class="emoji list-inline-item"><i class="em em-cry"></i></li>
                    <li class="emoji list-inline-item"><i class="em em-full_moon_with_face"></i></li>
                </ul>
            </div>
            <a href="#" class="d-flex align-items-center fw-600 text-grey-900 text-dark lh-26 font-xssss"><i class="feather-message-circle text-dark text-grey-900 btn-round-sm font-lg"></i><span class="d-none-xss">22 Comment</span></a>
            <a href="#" class="ms-auto d-flex align-items-center fw-600 text-grey-900 text-dark lh-26 font-xssss"><i class="feather-share-2 text-grey-900 text-dark btn-round-sm font-lg"></i><span class="d-none-xs">Share</span></a>
        </div>
    </div>`

        return html;
    }
}

class PostCardImage extends PostCardGenerator {
    getCard(data) {
        const html = `<div class="card w-100 shadow-xss rounded-xxl border-0 p-4 mb-0 mb-3">
        <div class="card-body p-0 d-flex">
            <figure class="avatar me-3"><img src="${data.user.image}" alt="image" class="shadow-sm rounded-circle w45"></figure>
            <h4 class="fw-700 text-grey-900 font-xssss mt-1">${data.user.username} <span class="d-block font-xssss fw-500 mt-1 lh-3 text-grey-500">2 hour ago</span></h4>
            <a href="#" class="ms-auto"><i class="ti-more-alt text-grey-900 btn-round-md bg-greylight font-xss"></i></a>
        </div>
        <div class="card-body p-0 me-lg-5">
            <p class="fw-500 text-grey-500 lh-26 font-xssss w-100 mb-2">${data.content} <a href="#" class="fw-600 text-primary ms-2">See more</a></p>
        </div>
        <div class="card-body d-block p-0 mb-3">
            <div class="row ps-2 pe-2">
                <div class="col-sm-12 p-1"><a href="" data-lightbox="roadtr"><img src="${data.product_images[0].image}" class="rounded-3 w-100" alt="image"></a></div>
            </div>
        </div>
        <div class="card-body d-flex p-0">
            <a href="#" class="emoji-bttn d-flex align-items-center fw-600 text-grey-900 text-dark lh-26 font-xssss me-2"><i class="feather-thumbs-up text-white bg-primary-gradiant me-1 btn-round-xs font-xss"></i> <i class="feather-heart text-white bg-red-gradiant me-2 btn-round-xs font-xss"></i>2.8K Like</a>
            <div class="emoji-wrap">
                <ul class="emojis list-inline mb-0">
                    <li class="emoji list-inline-item"><i class="em em---1"></i> </li>
                    <li class="emoji list-inline-item"><i class="em em-angry"></i></li>
                    <li class="emoji list-inline-item"><i class="em em-anguished"></i> </li>
                    <li class="emoji list-inline-item"><i class="em em-astonished"></i> </li>
                    <li class="emoji list-inline-item"><i class="em em-blush"></i></li>
                    <li class="emoji list-inline-item"><i class="em em-clap"></i></li>
                    <li class="emoji list-inline-item"><i class="em em-cry"></i></li>
                    <li class="emoji list-inline-item"><i class="em em-full_moon_with_face"></i></li>
                </ul>
            </div>
            <a href="#" class="d-flex align-items-center fw-600 text-grey-900 text-dark lh-26 font-xssss"><i class="feather-message-circle text-dark text-grey-900 btn-round-sm font-lg"></i><span class="d-none-xss">22 Comment</span></a>
            <a href="#" class="ms-auto d-flex align-items-center fw-600 text-grey-900 text-dark lh-26 font-xssss"><i class="feather-share-2 text-grey-900 text-dark btn-round-sm font-lg"></i><span class="d-none-xs">Share</span></a>
        </div>
    </div>`

        return html;
    }
}

class PostCardImages extends PostCardGenerator {
    getCard(data) {
        const html = `<div class="card w-100 shadow-xss rounded-xxl border-0 p-4 mb-0 mb-3">
                    <div class="card-body p-0 d-flex">
                        <figure class="avatar me-3"><img src="${data.user.image}" alt="image" class="shadow-sm rounded-circle w45"></figure>
                        <h4 class="fw-700 text-grey-900 font-xssss mt-1">${data.user.username} <span class="d-block font-xssss fw-500 mt-1 lh-3 text-grey-500">2 hour ago</span></h4>
                        <a href="#" class="ms-auto"><i class="ti-more-alt text-grey-900 btn-round-md bg-greylight font-xss"></i></a>
                    </div>
                    <div class="card-body p-0 me-lg-5">
                        <p class="fw-500 text-grey-500 lh-26 font-xssss w-100">${data.content} <a href="#" class="fw-600 text-primary ms-2">See more</a></p>
                    </div>
                    <div class="card-body d-block p-0 mb-3">
                        <div class="row ps-2 pe-2">
                            ${data.product_images.slice(0, 2).map(product_image => {
                                return `
                                    <div class="col-xs-6 col-sm-6 p-1"><a href="" data-lightbox="roadtri"><img src="${product_image.image}" class="rounded-3 w-100" alt="image"></a></div>
                                `
                            }).join("")}
                        </div>
                        <div class="row ps-2 pe-2">
                            ${data.product_images.slice(2, 4).map(product_image => {
                                return `
                                    <div class="col-xs-4 col-sm-4 p-1"><a href="images/t-33.jpg" data-lightbox="roadtri"><img src="${product_image.image}" class="rounded-3 w-100" alt="image"></a></div>
                                `
                            }).join("")}
                        </div>
                    </div>
                    <div class="card-body d-flex p-0">
                        <a href="#" class="emoji-bttn d-flex align-items-center fw-600 text-grey-900 text-dark lh-26 font-xssss me-2"><i class="feather-thumbs-up text-white bg-primary-gradiant me-1 btn-round-xs font-xss"></i> <i class="feather-heart text-white bg-red-gradiant me-2 btn-round-xs font-xss"></i>2.8K Like</a>
                        <div class="emoji-wrap">
                            <ul class="emojis list-inline mb-0">
                                <li class="emoji list-inline-item"><i class="em em---1"></i> </li>
                                <li class="emoji list-inline-item"><i class="em em-angry"></i></li>
                                <li class="emoji list-inline-item"><i class="em em-anguished"></i> </li>
                                <li class="emoji list-inline-item"><i class="em em-astonished"></i> </li>
                                <li class="emoji list-inline-item"><i class="em em-blush"></i></li>
                                <li class="emoji list-inline-item"><i class="em em-clap"></i></li>
                                <li class="emoji list-inline-item"><i class="em em-cry"></i></li>
                                <li class="emoji list-inline-item"><i class="em em-full_moon_with_face"></i></li>
                            </ul>
                        </div>
                        <a href="#" class="d-flex align-items-center fw-600 text-grey-900 text-dark lh-26 font-xssss"><i class="feather-message-circle text-dark text-grey-900 btn-round-sm font-lg"></i><span class="d-none-xss">22 Comment</span></a>
                        <a href="#" class="ms-auto d-flex align-items-center fw-600 text-grey-900 text-dark lh-26 font-xssss"><i class="feather-share-2 text-grey-900 text-dark btn-round-sm font-lg"></i><span class="d-none-xs">Share</span></a>
                    </div>
                </div>`

        return html;
    }
}

class PostCardVideo extends PostCardGenerator {
    getCard(data) {
        const html = `<div class="card w-100 shadow-xss rounded-xxl border-0 p-4 mb-3">
                            <div class="card-body p-0 d-flex">
                                <figure class="avatar me-3"><img src="${data.user.image}" alt="image" class="shadow-sm rounded-circle w45"></figure>
                                <h4 class="fw-700 text-grey-900 font-xssss mt-1">${data.user.username} <span class="d-block font-xssss fw-500 mt-1 lh-3 text-grey-500">2 hour ago</span></h4>
                                <a href="#" class="ms-auto" id="dropdownMenu5" data-bs-toggle="dropdown" aria-expanded="false"><i class="ti-more-alt text-grey-900 btn-round-md bg-greylight font-xss"></i></a>
                                <div class="dropdown-menu dropdown-menu-start p-4 rounded-xxl border-0 shadow-lg" aria-labelledby="dropdownMenu5">
                                    <div class="card-body p-0 d-flex">
                                        <i class="feather-bookmark text-grey-500 me-3 font-lg"></i>
                                        <h4 class="fw-600 text-grey-900 font-xssss mt-0 me-4">Save Link <span class="d-block font-xsssss fw-500 mt-1 lh-3 text-grey-500">Add this to your saved items</span></h4>
                                    </div>
                                    <div class="card-body p-0 d-flex mt-2">
                                        <i class="feather-alert-circle text-grey-500 me-3 font-lg"></i>
                                        <h4 class="fw-600 text-grey-900 font-xssss mt-0 me-4">Hide Post <span class="d-block font-xsssss fw-500 mt-1 lh-3 text-grey-500">Save to your saved items</span></h4>
                                    </div>
                                    <div class="card-body p-0 d-flex mt-2">
                                        <i class="feather-alert-octagon text-grey-500 me-3 font-lg"></i>
                                        <h4 class="fw-600 text-grey-900 font-xssss mt-0 me-4">Hide all from Group <span class="d-block font-xsssss fw-500 mt-1 lh-3 text-grey-500">Save to your saved items</span></h4>
                                    </div>
                                    <div class="card-body p-0 d-flex mt-2">
                                        <i class="feather-lock text-grey-500 me-3 font-lg"></i>
                                        <h4 class="fw-600 mb-0 text-grey-900 font-xssss mt-0 me-4">Unfollow Group <span class="d-block font-xsssss fw-500 mt-1 lh-3 text-grey-500">Save to your saved items</span></h4>
                                    </div>
                                </div>
                            </div>
                            <div class="card-body p-0 mb-3 rounded-3 overflow-hidden">
                                <a href="default-video.html" class="video-btn">
                                    <video autoplay="" loop="" class="float-right w-100">
                                        <source src="${data.product_video.video}" type="video/mp4">
                                    </video>
                                </a>
                            </div>
                            <div class="card-body p-0 me-lg-5">
                                <p class="fw-500 text-grey-500 lh-26 font-xssss w-100 mb-2">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi nulla dolor, ornare at commodo non, feugiat non nisi. Phasellus faucibus mollis pharetra. Proin blandit ac massa sed rhoncus <a href="#" class="fw-600 text-primary ms-2">See more</a></p>
                            </div>
                            <div class="card-body d-flex p-0">
                                <a href="#" class="emoji-bttn d-flex align-items-center fw-600 text-grey-900 text-dark lh-26 font-xssss me-2"><i class="feather-thumbs-up text-white bg-primary-gradiant me-1 btn-round-xs font-xss"></i> <i class="feather-heart text-white bg-red-gradiant me-2 btn-round-xs font-xss"></i>2.8K Like</a>
                                <div class="emoji-wrap">
                                    <ul class="emojis list-inline mb-0">
                                        <li class="emoji list-inline-item"><i class="em em---1"></i> </li>
                                        <li class="emoji list-inline-item"><i class="em em-angry"></i></li>
                                        <li class="emoji list-inline-item"><i class="em em-anguished"></i> </li>
                                        <li class="emoji list-inline-item"><i class="em em-astonished"></i> </li>
                                        <li class="emoji list-inline-item"><i class="em em-blush"></i></li>
                                        <li class="emoji list-inline-item"><i class="em em-clap"></i></li>
                                        <li class="emoji list-inline-item"><i class="em em-cry"></i></li>
                                        <li class="emoji list-inline-item"><i class="em em-full_moon_with_face"></i></li>
                                    </ul>
                                </div>
                                <a href="#" class="d-flex align-items-center fw-600 text-grey-900 text-dark lh-26 font-xssss"><i class="feather-message-circle text-dark text-grey-900 btn-round-sm font-lg"></i><span class="d-none-xss">22 Comment</span></a>
                                <a href="#" class="ms-auto d-flex align-items-center fw-600 text-grey-900 text-dark lh-26 font-xssss"><i class="feather-share-2 text-grey-900 text-dark btn-round-sm font-lg"></i><span class="d-none-xs">Share</span></a>
                            </div>
                        </div>`
        return html
    }
}

// Фабрика для создания карточек
class PostCardFactory {
    static createCard(type, data) {
        switch (type) {
            case "image":
                return new PostCardImage().getCard(data);
            case "video":
                console.log(data)
                return new PostCardVideo().getCard(data);
            case "multi-image":
                return new PostCardImages().getCard(data);
            default:
                console.log(data)
                return new PostCardGenerator().getCard(data);
        }
    }
}

class Pagination  {
    constructor(fetcher, pageSize = 10) {
        this.fetcher = fetcher;
        this.currentPage = 1;
        this.pageSize = pageSize;
        this.isFetching = false;
    }

    async paginate(callback) {
        const scrollHandler = async (e) => {
            const { scrollHeight, scrollTop } = document.documentElement;
            const nearBottom = scrollHeight - (scrollTop + window.innerHeight) < 300;

            if(nearBottom && !this.isFetching) {
                this.isFetching = true;
                try {
                    const posts = await this.fetcher.fetchPosts(this.currentPage);
                    if(posts.length) {
                        this.currentPage += 1
                        callback(posts)
                    }
                } finally {
                    this.isFetching = false;
                }
            }
        }

        window.addEventListener("scroll", scrollHandler)
        return () => window.removeEventListener("scroll", scrollHandler);
    }
}

class Post {
    constructor(postList, pagination) {
        if (!(pagination instanceof Pagination)) {
            throw new Error("Invalid Pagination instance.");
        }
        if (!postList) {
            throw new Error("Post list container is required.");
        }

        this.pagination = pagination;
        this.postList = postList;
        this.fetcher = new PostFetching();

        this.init()
    }

    async init() {
        await this.loadInitialPosts()
        this.enableScrollPagination();
    }

    async loadInitialPosts() {
        try {
            const initialPosts = await this.fetcher.fetchPosts(this.pagination.currentPage);
            if(initialPosts.length) {
                this.pagination.currentPage += 1
                this.renderPosts(initialPosts)
            }
        } catch(error) {
            onsole.error("Failed to load initial posts:", error);
        }
    }

    enableScrollPagination() {
        this.pagination.paginate((posts) => this.renderPosts(posts));
    }

    renderPosts(posts = []) {
        posts.forEach(post => {
            const card = PostCardFactory.createCard(post.postType, post)
            this.postList.innerHTML += card
        })
    }
}

class PostClient extends Post {}
class PostServer extends Post {}

window.addEventListener("DOMContentLoaded", () => {
    const postListCard = document.querySelector("#post-list-card")
    const fetcher = new PostFetching();
    const pagination = new Pagination(fetcher);
    const post = new Post(postListCard, pagination)
})



