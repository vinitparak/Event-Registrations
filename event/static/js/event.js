const template = document.createElement('template')

template.innerHTML = `
	<style> @import "https://cdn.jsdelivr.net/npm/bulma@0.8.0/css/bulma.min.css";
		.card {
			margin: 20px;
		}
		.post-author, .post-time {
		    display: block;
		}
		.card-header-title {
		    padding: .75rem 1rem;
		    display: block;
		}
	</style>
		<div class="card">
			<header class="card-header">
			    <div class="card-header-title">
                    <h6 class="event-title title is-size-4"></h6>
                    <time class="event-time subtitle is-size-7"></time>
                </div>
                <div class="card-header-icon">
                    <button class="button is-success" id="register">Register</button>
                </div>
			</header>
			<div class="card-content">
				<div class="content">
					<p class="event-description">
					</p>
					<p class="event-no_of_attendees">
					</p>
				</div>
			</div>
			<div class="card-image">
				<figure class="image is-4by3">
					<img class="image" id="eventImage" alt="Placeholder image">
				</figure>
			</div>
		</div>
		`

class PostElement extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({mode: 'open'})
		this.template = template.content.cloneNode(true);
        this.shadowRoot.append(this.template);

        this.getPostData = this.getPostData.bind(this);
        this.addPostData = this.addPostData.bind(this);
    }

    connectedCallback() {

        let postId = this.getAttribute("id");
       	let postData = this.getPostData(postId);
       	this.addPostData(postData);

       	this.shadowRoot.querySelector('#register').addEventListener('click', e => {
       	    let edata;
       	    $.ajax({
       	        async: false,
       	        type: 'GET',
       	        url: '/registerevent/'+postId,
       	        success: function(data) {
       	            edata = data;
       	        }
       	    });
       	    console.log(edata);
       	});
    }

    addPostData(data) {
    	let tags = ['title', 'description', 'time', 'no_of_attendees'];
    	for(var i=0; i<tags.length; i++)
    	    if(data.hasOwnProperty(tags[i])) {
    		    this.shadowRoot.querySelectorAll('.event-'+tags[i]).forEach(e => e.innerHTML = data[tags[i]]);
    		} else {
    		    this.shadowRoot.querySelectorAll('.event-'+tags[i]).forEach(e => e.setAttribute('style', 'display: none'));
    		}

    	if(data.hasOwnProperty('image'))
    	    this.shadowRoot.querySelector("#eventImage").setAttribute('src', 'media/'+data['image']);
    	else
    	    this.shadowRoot.querySelector(".image").setAttribute('style', 'display: none');
    }

    getPostData(postId) {
        let postData;
        $.ajax({
            async: false,
            type: 'GET',
            url: '/event/'+postId,
            success: function(data) {
                postData = data;
            }
        });
        console.log(postData);
        return postData;
    }
}

(function() {
    $.get(
        "total/",
        function(data) {
            data = data['count']
            for (var i=0; i<data.length; i++) {
                var e = document.createElement('post-element');
                e.setAttribute("id", data[i]);
                document.getElementById("posts").appendChild(e);
            }
        }
    )
})();

window.customElements.define("post-element", PostElement);