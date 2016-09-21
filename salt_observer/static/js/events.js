$(function() {

    // ATTENTION: set the token before importing this script

    var socket = new WebSocket('wss://' + host + ':' + port + '/all_events/' + token);

    // Get Salt's "real time" event stream.
    socket.onopen = function() {
        socket.send('websocket client ready');
        console.log('Connected!');
        $('#conn_status').html('<i class="fa fa-fw fa-check"></i> Connected!');
    };

    // Other handlers
    socket.onerror = function(event) {
        console.debug('Error!', event);
        $('#conn_status').html('<i class="fa fa-fw fa-times"></i> Connection failed!');
    };

    // event.data represents Salt's "real time" event data as serialized JSON.
    socket.onmessage = function(event) {
        var event = processEvent(event);

        if (event.tag.startsWith('salt/job/')) {
            addJob(event);
        } else {
            addEvent(event);
        }
    };

    var severity_level = {
        0: {name: 'debug', icon: 'bug'},
        10: {name: 'info', icon: 'info'},
        20: {name: 'success', icon: 'check'},
        30: {name: 'warning', icon: 'exclamation-triangle'},
        40: {name: 'critical', icon: 'times'},
    };

    function processEvent(raw_event) {
        var event = JSON.parse(raw_event.data.substring(6));

        if ("data" in event.data) {
            // an event that was fired via engine
            event.title = event.data.data.title;
            event.message = event.data.data.message.substring(0,300) + '[...]';
            event.severity = severity_level[event.data.data.severity];
        } else {
            // an event that is fired by salt internals
            event.title = event.data.id;
            event.message = '<pre>' + JSON.stringify(event) + '</pre>';
            event.severity = severity_level[0];
        }

        return event;
    };

    function addEvent(event) {
        var tpl = $('#event-template').clone();
        tpl.removeAttr('id');
        tpl.addClass('severity-' + event.severity.name);
        tpl.find('.icon').html('<i class="event-icon fa fa-fw fa-2x fa-' + event.severity.icon + '"></i>')
        tpl.find('.title').text(event.title);

        var messagebox_id = event.data._stamp.replace(/(\.|\:|\-)+/g, '');

        tpl.find('.collapse-link a').attr('href', '#' + messagebox_id);
        tpl.find('.message')
            .html(event.message)
            .attr('id', messagebox_id)
            .on('show.bs.collapse', function() {$(this).parent().find('.collapse-link i').removeClass('fa-chevron-right').addClass('fa-chevron-down');})
            .on('hide.bs.collapse', function() {$(this).parent().find('.collapse-link i').removeClass('fa-chevron-down').addClass('fa-chevron-right');});

        tpl.find('.tag').text(event.tag);
        tpl.find('.minion-id').text(event.data.id);
        tpl.find('.timestamp').text(Date(event.data._stamp));
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
