$(function() {

    // ATTENTION: set the token before importing this script

    var socket = new WebSocket('ws://localhost:8002/all_events/' + token);

    // Get Salt's "real time" event stream.
    socket.onopen = function() {
        socket.send('websocket client ready');
        console.log('Connected!');
        $('#conn_status').html('<i class="fa fa-fw fa-check"></i> Connected!');
    };

    // Other handlers
    socket.onerror = function(e) {
        console.debug('Error!', e);
        $('#conn_status').html('<i class="fa fa-fw fa-times"></i> Connection failed!');
    };

    // e.data represents Salt's "real time" event data as serialized JSON.
    socket.onmessage = function(e) {
        console.log(e);
        //var data = $.parseJSON(e.data.substring(6));
        var data = JSON.parse(e.data.substring(6));

        if (data.tag.startsWith('salt/job/')) {
            addJob(data);
        } else {
            addEvent(data);
        };
    };

    function addEvent(event) {
        var tpl = $('#event-template').clone();
        tpl.removeAttr('id');
        tpl.find('.icon').html('<i class="fa fa-fw fa-2x fa-bug"></i>')
        tpl.find('.title').text(event.data.id);
        tpl.find('.message').html('<pre>' + JSON.stringify(event.data) + '</pre>');
        tpl.find('.tag').text(event.tag);
        tpl.find('.minion-id').text(event.data.id);
        $('#eventholder').prepend(tpl);

        setTimeout(function() {
            tpl.remove();
        }, 300000);
    };

    function addJob(data) {
        var tpl = $('#job-template').clone();
        tpl.removeAttr('id');
        tpl.find('.timestamp').text(data.data._stamp);
        tpl.find('.tag').text(data.tag);
        $('#jobholder').prepend(tpl);

        setTimeout(function() {
            tpl.remove()
        }, 60000);
    };
});
