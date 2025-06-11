let editingPostId = null; // Track whether we are editing an existing post

// Function that runs once the window is fully loaded
window.onload = function() {
    // Attempt to retrieve the API base URL from the local storage
    var savedBaseUrl = localStorage.getItem('apiBaseUrl');
    // If a base URL is found in local storage, load the posts
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
}

// Function to fetch all the posts from the API and display them on the page
function loadPosts() {
    // Retrieve the base URL from the input field and save it to local storage
    var baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);

    console.log("Loading posts from:", baseUrl + '/posts');

    // Use the Fetch API to send a GET request to the /posts endpoint
    fetch(baseUrl + '/posts')
        .then(response => response.json())  // Parse the JSON data from the response
        .then(data => {  // Once the data is ready, we can use it
            console.log('Fetched posts:', data);
            // Clear out the post container first
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            // For each post in the response, create a new post element and add it to the page
            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `<h2>${post.title}</h2><p>${post.content}</p>
                <button onclick="startEdit(${post.id}, '${escapeStr(post.title)}', '${escapeStr(post.content)}')">Edit</button>
                <button onclick="deletePost(${post.id})">Delete</button>`;
                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Helper function to safely pass content into JS event handlers
function escapeStr(str) {
    return str.replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

// Function to send a POST request to the API to add a new post
function addOrUpdatePost() {   // previously addPost()
    // Retrieve the values from the input fields
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;

    // For Updating an existing Post
    const method = editingPostId ? 'PUT' : 'POST';
    const endpoint = editingPostId ? `${baseUrl}/posts/${editingPostId}` : `${baseUrl}/posts`;

    fetch(endpoint, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: postTitle, content: postContent })
    })

    // Use the Fetch API to send a POST request to the /posts endpoint
//    fetch(baseUrl + '/posts', {
//        method: 'POST',
//        headers: { 'Content-Type': 'application/json' },
//        body: JSON.stringify({ title: postTitle, content: postContent })
//    })
    //.then(response => response.json())  // Parse the JSON data from the response

    .then(async response => {
        const data = await response.json();
        if (!response.ok) {
            // Show error message in the UI
            document.getElementById('error-message').textContent = data.error || 'An unknown error occurred.';
            throw new Error(data.error || 'Request failed');
        }
        // Clear any existing error
        document.getElementById('error-message').textContent = '';
        return data;
    })

    .then(post => {
        console.log('Post added:', post);
        loadPosts(); // Reload the posts after adding a new one
        resetForm();
        // Added - clear form fields
//        document.getElementById('post-title').value = '';
//        document.getElementById('post-content').value = '';
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a PUT request to the API to update a post
function startEdit(postId, title, content) {
    editingPostId = postId;
    document.getElementById('post-title').value = title;
    document.getElementById('post-content').value = content;
    document.getElementById('submit-button').textContent = 'Update Post';
    document.getElementById('cancel-edit-button').style.display = 'inline-block';
}

// Helper Function to clear form fields after insertion
function resetForm() {
    editingPostId = null;
    document.getElementById('post-title').value = '';
    document.getElementById('post-content').value = '';
    document.getElementById('submit-button').textContent = 'Add Post';
    document.getElementById('cancel-edit-button').style.display = 'none';
}

// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;

    // Use the Fetch API to send a DELETE request to the specific post's endpoint
    fetch(baseUrl + '/posts/' + postId, {
        method: 'DELETE'
    })

    .then(response => response.json().then(data => ({ status: response.status, body: data })))
    .then(result => {
        const messageDiv = document.getElementById('message');
        if (result.status === 200) {
            messageDiv.innerText = result.body.message;
            messageDiv.style.color = "green";
            // Auto-hide the message after 3-5 seconds
            setTimeout(() => {
                messageDiv.innerText = '';
            }, 4000);

        } else {
            messageDiv.innerText = result.body.error || "Something went wrong.";
            messageDiv.style.color = "red";
        }
    //.then(response => {
    //    console.log('Post deleted:', postId);
        loadPosts(); // Reload the posts after deleting one
    })
    .catch(error => {
    console.error('Error:', error);  // If an error occurs, log it to the console
    document.getElementById('message').innerText = "An error occurred.";
    document.getElementById('message').style.color = "red";
    });
}