var mousePressed = false;
var lastX, lastY;
var canvas;
var ctx;

function InitThis() {
    canvas = document.getElementById('myCanvas');
    ctx = canvas.getContext("2d");

    $('#myCanvas').mousedown(function (e) {
        mousePressed = true;
        Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, false);
    });

    $('#myCanvas').mousemove(function (e) {
        if (mousePressed) {
            Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, true);
        }
    });

    $('#myCanvas').mouseup(function (e) {
        mousePressed = false;
    });

    $('#myCanvas').mouseleave(function (e) {
        mousePressed = false;
    });

    // const image = new Image(60, 45); // Using optional size for image

    // image.onload = drawImageActualSize; // Draw when image has loaded
    //
    // // Load an image of intrinsic size 300x227 in CSS pixels
    // image.src = '/static/img/dino.jpg';
    //
    // function drawImageActualSize() {
    //   // Will draw the image as 300x227, ignoring the custom size of 60x45
    //   // given in the constructor
    //   ctx.drawImage(this, 0, 0);
    //
    //   // To use the custom size we'll have to specify the scale parameters
    //   // using the element's width and height properties - lets draw one
    //   // on top in the corner:
    //   ctx.drawImage(this, 0, 0, this.width, this.height);
    // }
}

function Draw(x, y, isDown) {
    if (isDown) {
        ctx.beginPath();
        ctx.strokeStyle = $('#selColor').val();
        ctx.lineWidth = $('#selWidth').val();
        if ($('#selColor').val() === "rgba(255,255,255,0)") {
            console.log($('#selColor').val());
            ctx.globalCompositeOperation = "destination-out";
        }
        ctx.lineJoin = "round";
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(x, y);
        ctx.closePath();
        ctx.stroke();
    }
    lastX = x; lastY = y;
}

function clearArea() {
    // Use the identity matrix while clearing the canvas
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
}

function putImage() {
    var fileId = document.getElementById('fileId').innerHTML;
    var fileExtension = document.getElementById('fileExtension').innerHTML;
    var dataURL = canvas.toDataURL('image/png');
    console.log(dataURL);
    $.ajax({
      type: "POST",
      url: "/drawer/",
      data: {
          imgBase64: dataURL,
          filename: 'static/media/' + fileId + '-checked.' + fileExtension,
          fileId: fileId,
      }
    }).done(function(o) {
      console.log('saved');
      // If you want the file to be visible in the browser
      // - please modify the callback in javascript. All you
      // need is to return the url to the file, you just saved
      // and than put the image in your browser.
    });
}