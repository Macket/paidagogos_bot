var fitImageOn = function(canvas, context, imageObj) {
	var imageAspectRatio = imageObj.width / imageObj.height;
	var canvasAspectRatio = canvas.width / canvas.height;
	var renderableHeight, renderableWidth, xStart, yStart;

	// If image's aspect ratio is less than canvas's we fit on height
	// and place the image centrally along width
	if(imageAspectRatio < canvasAspectRatio) {
		renderableHeight = canvas.height;
		renderableWidth = imageObj.width * (renderableHeight / imageObj.height);
		xStart = (canvas.width - renderableWidth) / 2;
		yStart = 0;
	}

	// If image's aspect ratio is greater than canvas's we fit on width
	// and place the image centrally along height
	else if(imageAspectRatio > canvasAspectRatio) {
		renderableWidth = canvas.width;
		renderableHeight = imageObj.height * (renderableWidth / imageObj.width);
		xStart = 0;
		yStart = (canvas.height - renderableHeight) / 2;
	}

	// Happy path - keep aspect ratio
	else {
		renderableHeight = canvas.height;
		renderableWidth = canvas.width;
		xStart = 0;
		yStart = 0;
	}
	context.drawImage(imageObj, xStart, yStart, renderableWidth, renderableHeight);
};

function placeImage() {
    var canvas = document.getElementById('myCanvas');
    var context = canvas.getContext('2d');
    var imageObj = new Image();


    var fileId = document.getElementById('fileId').innerHTML;
    var fileExtension = document.getElementById('fileExtension').innerHTML;
    imageObj.src = '/static/media/' + fileId + '.' + fileExtension;

    imageObj.onload = function() {
        fitImageOn(canvas, context, imageObj)
    };
}