/**
 * Bounding Box Annotation Tool.
 */

var MENU_WIDTH = 200;
var ZOOM_STEP = 0.2;
var CIRCLE_RADIUS = 20;

var currentZoomLevel = -0.5;
var moveOrigin = null;

var imageObject = null;
var tags = [];

var canvas = new fabric.Canvas('canvas', {
    width: window.innerWidth - MENU_WIDTH,
    height: window.innerHeight,
    selection: false,
});

fabric.Image.fromURL(config.imageUrl, function(image) {
    var scale = canvas.width / image.width;
    image.set({
        hasControls: false,
        hasRotatingPoint: false,
        hasBorders: false,
        selectable: false,
        evented: false,
        scaleX: scale,
        scaleY: scale,
    });

    imageObject = image;
    canvas.add(image);
});

canvas.on('mouse:down', function(options) {
    moveOrigin = canvas.getPointer(options.e, true);
});

canvas.on('mouse:up', function() {
    moveOrigin = null;
});

canvas.on('mouse:move', function(options) {
    if(!moveOrigin) {
        return;
    }

    var pointer = canvas.getPointer(options.e, true);
    canvas.relativePan(new fabric.Point(pointer.x - moveOrigin.x, pointer.y - moveOrigin.y));
    moveOrigin = pointer;
});

canvas.on('mouse:dblclick', function(options) {
    var pointer = canvas.getPointer(options.e, false);

    var value = prompt('Enter decimal value.');
    if(value === null || value.trim() === '') {
        return;
    }

    value = value.trim();
    var circle = new fabric.Circle({
        hasControls: false,
        hasRotatingPoint: false,
        hasBorders: false,
        selectable: false,
        evented: false,
        left: pointer.x - CIRCLE_RADIUS,
        top: pointer.y - CIRCLE_RADIUS,
        radius: CIRCLE_RADIUS,
        fill: 'rgba(255,0,0,0.5)',
    });

    canvas.add(circle);
    tags.push({
        object: circle,
        value: value,
    });
});

$('main').on('mousewheel', function(options) {
    var delta = options.originalEvent.wheelDelta;
    if(delta === 0) {
        return;
    }

    var pointer = canvas.getPointer(options.e, true);
    var point = new fabric.Point(pointer.x, pointer.y);

    if(delta > 0) {
        currentZoomLevel += ZOOM_STEP;
    } else {
        currentZoomLevel -= ZOOM_STEP;
    }

    canvas.zoomToPoint(point, Math.pow(2, currentZoomLevel));
});

$(window).resize(function() {
    canvas.setWidth(window.innerWidth - MENU_WIDTH);
    canvas.setHeight(window.innerHeight);
});

$(document).ready(function() {
    canvas.zoomToPoint(new fabric.Point(0, 0), Math.pow(2, currentZoomLevel));
});

$('#reset-view').on('click', function() {
    currentZoomLevel = 0.0;
    canvas.setViewportTransform([1, 0, 0, 1, 0, 0]);
});

$('#clear-tags').on('click', function() {
    tags.forEach(function(t) {
        canvas.remove(t.object);
    });

    tags = [];
});

$('#submit-hit').on('click', function() {
    var url = turkGetSubmitToHost();
    var id = turkGetParam('assignmentId', '');

    var annotations = JSON.stringify(tags.map(function(t) {
        return {
            x: t.object.left + CIRCLE_RADIUS,
            y: t.object.top + CIRCLE_RADIUS,
            value: t.value,
        };
    }));

    alert(url);
    alert(id);
    alert(annotations);

    document.getElementById('assignmentId').value = id;
    document.getElementById('annotations').value = annotations;

    var form = $('#mturk_form');

    form.attr('action', url + '/mturk/externalSubmit');
    form.submit();
});

