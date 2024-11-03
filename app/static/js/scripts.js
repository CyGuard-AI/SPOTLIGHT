document.addEventListener('DOMContentLoaded', function() {
    displayCurrentDate();
});

function joinVisit(visitId) {
    alert('You have joined this visit!');
    // Notify all participants here
}

document.querySelectorAll('.comment-form').forEach(form => {
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const visitId = this.getAttribute('data-visit-id');
        const commentInput = this.querySelector('.comment-input');
        const comment = commentInput.value;
        fetch('/add_comment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ visit_id: visitId, comment: comment })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            loadComments(visitId);
            commentInput.value = '';
        })
        .catch(error => console.error('Error:', error));
    });
});

function loadComments(visitId) {
    fetch(`/get_comments/${visitId}`)
    .then(response => response.json())
    .then(data => {
        const commentsDiv = document.getElementById(`comments-${visitId}`);
        commentsDiv.innerHTML = '';
        data.forEach(comment => {
            const commentItem = document.createElement('div');
            commentItem.textContent = comment.comment;
            commentsDiv.appendChild(commentItem);
        });
    })
    .catch(error => console.error('Error:', error));
}

function displayCurrentDate() {
    const currentDate = new Date();
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    document.getElementById('current-date').textContent = currentDate.toLocaleDateString('en-US', options);
}
