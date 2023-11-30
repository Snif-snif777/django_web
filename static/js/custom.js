function showLoadingSpinner() {
    // Add code to show loading spinner
    // For example, you can use a library like Font Awesome for the spinner icon
    document.querySelector('.btn.btn-primary.btn-block').innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
}

function showDeleteConfirmation(event) {
    event.preventDefault();

    // Create a modal dialog
    var modalHtml = `
        <div class="modal fade" id="deleteConfirmationModal" tabindex="-1" role="dialog" aria-labelledby="deleteConfirmationModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="deleteConfirmationModalLabel">Confirmation</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <p>Are you sure you want to delete this item?</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary" data-dismiss="modal">Cancel</button>
                        <a href="${event.target.href}" class="btn btn-danger">Delete</a>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Append the modal to the body
    $('body').append(modalHtml);

    // Show the modal
    $('#deleteConfirmationModal').modal('show');
}