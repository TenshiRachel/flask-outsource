// Files-Table DataTable
$(function() {
    if ($('#files-table').length > 0) {
        function filesTableInit(tableId) {
            let focus = $(tableId);

            let path = window.location.pathname.slice(1);
            path = path.slice(path.indexOf('/') + 1);

            if (path === 'share-drive') {
                focus.find('th#shared').remove();
                focus.find('td[headers="shared"').remove();
            }

            focus.DataTable({
                ordering: true,
                order: [[1, 'asc']],
                paging: false,
                info: false,
                searching: false,
                language: { emptyTable: 'No files or folders to display' },
                columnDefs: [{
                    orderable: false,
                    targets: 0
                }],
            });

            if (focus.find('.dataTables_empty').length > 0) {
                focus.find('#check-all').prop('disabled', true);
            }
            else {
                focus.find('#check-all').prop('disabled', false);
            }
        }

        filesTableInit("#files-table");

        let rows = $('tbody tr', '#files-table');
        let i = 1;

        $('.table-responsive').addClass('overflow-x-hidden');
        $(rows[0]).removeClass('d-none');
        $(rows[0]).addClass('flipInX').one('animationend', function() {
            $(this).removeClass('flipInX');
            $(this).removeClass('d-none');
        });

        setInterval(function() {
            $(rows[i]).removeClass('d-none');
            $(rows[i]).addClass('flipInX').one('animationend', function() {
                $(this).removeClass('flipInX');
            });

            i++;

            if (i === rows.length) {
                setTimeout(function() {
                    $('.table-responsive').removeClass('overflow-x-hidden');

                    clearTimeout(this);
                }, 500);

                clearInterval(this);
            }
        }, 250);

        $(window).on('resize', function () {
            $('#files-table').DataTable().destroy();
            filesTableInit('#files-table');
        });

        // Checkboxes
        let focuses = $('input[type="checkbox"][name="fid"]', '#files-table');
        let checked = focuses.filter(':checked');

        if (checked.length > 0) {
            setTimeout(function() {
                $(focuses[0]).trigger('change');

                clearTimeout(this);
            }, 250);
        }

        $('input#check-all', '#files-table').on('change', function() {
            if ($(this).prop('checked') === true) {
                focuses.prop('checked', true);
            }
            else {
                focuses.prop('checked', false);
            }

            $(focuses[0]).trigger('change');
        });

        focuses.on('change', function() {
            let checkboxAll = $('#check-all', '#files-table').last();
            let focus = $('.select-actions', '#mobile-action-menu, #action-card');
            let singleActions = focus.find('.single-select');
            let selectCount = focus.find('.select-count');
            let checked = focuses.filter(':checked');
            let count = checked.length;

            if (count >= focuses.length) {
                checkboxAll.prop('checked', true);
            }
            else {
                checkboxAll.prop('checked', false);
            }

            if (count < 1) {
                selectCount.html(`${count} Item Selected`);
            }

            if (count > 0) {
                focus.each(function() {
                    _this = $(this);

                    if (_this.hasClass('d-none')) {
                        _this.removeClass('d-none');

                        if (_this.hasClass('animated')) {

                            _this.addClass('flipInX').one('animationend', function() {
                                $(this).removeClass('flipInX');
                            });
                        }
                    }
                });

                // Google Upload
                let googleCopy = focus.find('.google-copy');
                let flag = true;

                checked.each(function() {
                    if ($(this).attr('data-type') === 'folder') flag = false;
                });

                googleCopy.each(function() {
                    _this = $(this);

                    if (flag && _this.hasClass('d-none')) {
                        _this.removeClass('d-none');

                        if (_this.hasClass('animated')) {
                            _this.addClass('flipInX').one('animationend', function() {
                                $(this).removeClass('flipInX');
                            });
                        }
                    }
                    else if (!flag && !_this.hasClass('d-none')) {
                        if (_this.hasClass('animated')) {
                            _this.addClass('flipOutX').one('animationend', function() {
                                let _this = $(this);

                                _this.addClass('d-none');
                                _this.removeClass('flipOutX');
                            });
                        }
                        else {
                            _this.addClass('d-none');
                        }
                    }
                });

                selectCount.html(`${count} Item Selected<i class="far fa-check ml-2"></i>`);

                // Download link and Edit Link
                if (count === 1) {
                    let downloadAction = singleActions.find('form.download');
                    let editAction = singleActions.find('a.edit');
                    let type = checked.last().attr('data-type');

                    downloadAction.attr('action', `/files/download/${checked.last().attr('data-id')}`);

                    if (type === 'code' || type === 'image') {
                        editAction.attr('href', `${window.location.pathname}/${checked.last().attr('data-id')}/~edit`);
                        editAction.removeClass('d-none');
                    }
                    else {
                        editAction.addClass('d-none');
                    }
                }

                if (count > 1) {
                    selectCount.html(`${count} Items Selected<i class="far fa-check ml-2"></i>`);

                    singleActions.each(function() {
                        _this = $(this);

                        if (!_this.hasClass('d-none')) {
                            if (_this.hasClass('animated')) {
                                _this.addClass('flipOutX').one('animationend', function() {
                                    $(this).addClass('d-none');
                                    $(this).removeClass('flipOutX');
                                });
                            }
                            else {
                                _this.addClass('d-none');
                            }
                        }
                    });
                }
                else {
                    singleActions.each(function() {
                        _this = $(this);

                        if (_this.hasClass('d-none')) {
                            if (_this.hasClass('animated')) {
                                _this.removeClass('d-none');

                                _this.addClass('flipInX').one('animationend', function() {
                                    $(this).removeClass('flipInX');
                                });
                            }
                            else {
                                _this.removeClass('d-none');
                            }
                        }
                    });
                }
            }
            else {
                focus.each(function() {
                    _this = $(this);

                    if (!_this.hasClass('d-none')) {
                        if (_this.hasClass('animated')) {
                            _this.addClass('flipOutX').one('animationend', function() {
                                $(this).addClass('d-none');
                                $(this).removeClass('flipOutX');
                            });
                        }
                        else {
                            _this.addClass('d-none');
                        }
                    }
                });

                singleActions.each(function() {
                    _this = $(this);

                    if (!_this.hasClass('d-none')) {
                        if (_this.hasClass('animated')) {
                            _this.addClass('flipOutX').one('animationend', function() {
                                $(this).addClass('d-none');
                                $(this).removeClass('flipOutX');
                            });
                        }
                        else {
                            _this.addClass('d-none');
                        }
                    }
                });
            }
        });
    }
});

// Rename and Share Modal
$('#rename-modal, #share-modal').on('show.bs.modal', function() {
        let modalId = $(this).attr('id');
        let form = $(this).find('form');
        let td = $('td[headers="select"] input:checked', '#files-table').last();

        form.find('input[name="fid"]', `#${modalId}`).val(td.attr('data-id'));

        if (modalId === 'rename-modal') {
            let input = form.find('input[name="rename"]');

            if (td.attr('data-name')) {
                let name = td.attr('data-name');
                name = name.slice(0, (name.lastIndexOf('.') > 0 ? name.lastIndexOf('.') : name.length));

                if (!input.val()) {
                    input.val(name);
                }

                input.next().addClass('active');
            }
        }
        else if (modalId === 'share-modal') {
            let share = {
                uids: td.attr('data-share-uids'),
                usernames: td.attr('data-share-usernames'),
                emails: td.attr('data-share-emails')
            };

            if (share['uids'] && share['usernames'] && share['emails']) {
                let table = $('#share-users-table', '#share-modal');
                let tbody = $('<tbody></tbody>');

                table.find('tbody').remove();

                share['uids']  = share['uids'].split(',');
                share['usernames'] = share['usernames'].split(',');
                share['emails'] = share['emails'].split(',');

                $('.share-users', '#share-modal').removeClass('d-none');

                for (let i = 0, n = share['uids'].length; i < n; i++) {
                    let roundedLeft = i >= n - 1 ? ' class="rounded-bottom-left"' : '';
                    let roundedRight = i >= n - 1 ? ' class="rounded-bottom-right"' : '';
                    let uid = share['uids'][i];
                    let username = share['usernames'][i];
                    let email = share['emails'][i];

                    tbody.append(`
                        <tr>
                            <td headers="share-select"${roundedLeft}>
                                <div class="form-check">
                                    <input id="su-${uid}" class="form-check-input" type="checkbox" name="uid" value="${uid}">
                                    <label class="form-check-label" for="su-${uid}"></label>
                                </div>
                            </td>
                            <td headers="share-username">
                                ${username}
                            </td>
                            <td headers="share-email"${roundedRight}>
                                ${email}
                            </td>
                        </tr>
                    `);
                }

                table.append(tbody);

                // Init or Re-init DataTable
                table.DataTable().destroy();

                table.DataTable({
                    ordering: true,
                    order: [[1, 'asc']],
                    paging: false,
                    info: false,
                    searching: false,
                    language: { emptyTable: 'Not shared with any user yet.' },
                    columnDefs: [{
                        orderable: false,
                        targets: 0
                    }],
                });

                // Checkboxes
                let checkall = table.find('#check-all-share-user');
                let checkboxes = table.find('td[headers="share-select"] input[type="checkbox"]');

                checkboxes.on('change', function() {
                    let removeBtn = $('.share-users button[type="submit"]', '#share-modal');
                    let checked = checkboxes.filter(':checked');
                    let count = checked.length;

                    if (count > 0) {
                        if (removeBtn.hasClass('d-none')) {
                            removeBtn.removeClass('d-none');

                            removeBtn.addClass('bounceIn').one('animationend', function() {
                                $(this).removeClass('bounceIn');
                            });
                        }
                    }
                    else {
                        removeBtn.addClass('bounceOut').one('animationend', function() {
                            $(this).addClass('d-none');
                            $(this).removeClass('bounceOut');
                        });
                    }

                    if (count >= checkboxes.length) {
                        checkall.prop('checked', true);
                    }
                    else {
                        checkall.prop('checked', false);
                    }
                });

                // Check All
                checkall.on('click', function() {
                    let _this = $(this);

                    if (_this.prop('checked')) {
                        _this.prop('checked', true);
                        checkboxes.prop('checked', true);
                    }
                    else {
                        _this.prop('checked', false);
                        checkboxes.prop('checked', false);
                    }

                    $(checkboxes[0]).trigger('change');
                });
            }
            else {
                $('.share-users', '#share-modal').addClass('d-none');
            }

            // Share Code
            let code = td.attr('data-share-code') ? td.attr('data-share-code') : null;

            if (code) {
                let footer = $(this).find('.modal-footer');
                let left = footer.find('.text-left:not(.text-md-right)', '.row');
                let right = footer.find('.text-md-right', '.row');

                let url = `${window.location.host}/files/${code}/~shared`;

                // Left-Col
                let icon = left.find('i').clone();
                icon.removeClass('fa-unlink');
                icon.addClass('fa-link');

                left.html(`
                    ${icon[0].outerHTML}
                    <span class="align-middle cursor-default material-tooltip-sm" data-tooltip="tooltip" data-placement="bottom" title="${url}">
                        Share link created
                    </span>
                `);

                $('[data-tooltip="tooltip"].material-tooltip-sm').tooltip({
                    template: '<div class="tooltip md-tooltip"><div class="tooltip-arrow md-arrow"></div><div class="tooltip-inner md-inner"></div></div>'
                });

                // Right-Col
                right.html(`
                    <button class="btn btn-md btn-primary m-0 waves-effect waves-light" type="button">
                        <i class="far fa-clipboard mr-2"></i>Copy Link
                    </button>
                    <button class="btn btn-md btn-danger m-0 waves-effect waves-light" type="submit">
                        <i class="far fa-unlink mr-2"></i>Remove Share Link
                    </button>
                `);

                let copyBtn = right.find('button[type="button"]');

                copyBtn.on('click', function() {
                    let focus = $('.modal-footer', '#share-modal');
                    focus.append(`<input type="text" name="clipboard" value="${url}">`);

                    let clipboardInput = focus.find('input[name="clipboard"]');
                    clipboardInput.select();
                    document.execCommand('copy');
                    clipboardInput.remove();

                    toastr['success']('Share link copied.', null, {
                        'closeButton': true,
                        'progressBar': true,
                        'newestOnTop': true,
                        'hideDuration': 300,
                        'timeOut': 2000,
                        'extendedTimeOut': 1000
                    });
                });
            }
        }
});

// Search
$(function() {
    let searchInput = $('input[name="search"]');
    let trs = $('tbody tr', '#files-table');

    let filterCheckboxes = $('.filter-all, .filter-name, .filter-size, .filter-type, .filter-shared, .filter-modified');
    let filters = ['name', 'size', 'type', 'shared', 'modified'];

    // Filters
    $('.search-filters').on('click', function() {
        return false;
    });

    filterCheckboxes.parent().on('click', function() {
        let checkbox = $(this).children('input[type="checkbox"]');

        if (checkbox.is(':checked')) {
            if (checkbox.hasClass('filter-all')) {
                $('.filter-all').prop('checked', false);
                $('.filter-name').prop('checked', false);
                $('.filter-size').prop('checked', false);
                $('.filter-type').prop('checked', false);
                $('.filter-shared').prop('checked', false);
                $('.filter-modified').prop('checked', false);

                filters = [];
            }
            else {
                $('.filter-all').prop('checked', false);

                if (checkbox.hasClass('filter-name')) {
                    $('.filter-name').prop('checked', false);

                    filters.splice($.inArray('name', filters), 1);
                }
                else if (checkbox.hasClass('filter-size')) {
                    $('.filter-size').prop('checked', false);

                    filters.splice($.inArray('size', filters), 1);
                }
                else if (checkbox.hasClass('filter-type')) {
                    $('.filter-type').prop('checked', false);

                    filters.splice($.inArray('type', filters), 1);
                }
                else if (checkbox.hasClass('filter-shared')) {
                    $('.filter-shared').prop('checked', false);

                    filters.splice($.inArray('shared', filters), 1);
                }
                else if (checkbox.hasClass('filter-modified')) {

                    $('.filter-modified').prop('checked', false);

                    filters.splice($.inArray('modified', filters), 1);
                }
            }
        }
        else {
            if (checkbox.hasClass('filter-all')) {
                checkbox.prop('checked', true);
                $('.filter-all').prop('checked', true);
                $('.filter-name').prop('checked', true);
                $('.filter-size').prop('checked', true);
                $('.filter-type').prop('checked', true);
                $('.filter-shared').prop('checked', true);
                $('.filter-modified').prop('checked', true);

                filters = ['name', 'size', 'type', 'shared', 'modified'];
            }
            else {
                if (checkbox.hasClass('filter-name')) {
                    $('.filter-name').prop('checked', true);

                    if (!filters.includes('name')) {
                        filters.push('name');
                    }
                }
                else if (checkbox.hasClass('filter-size')) {
                    $('.filter-size').prop('checked', true);

                    if (!filters.includes('size')) {
                        filters.push('size');
                    }
                }
                else if (checkbox.hasClass('filter-type')) {
                    $('.filter-type').prop('checked', true);

                    if (!filters.includes('type')) {
                        filters.push('type');
                    }
                }
                else if (checkbox.hasClass('filter-shared')) {
                    $('.filter-shared').prop('checked', true);

                    if (!filters.includes('shared')) {
                        filters.push('shared');
                    }
                }
                else if (checkbox.hasClass('filter-modified')) {
                    $('.filter-modified').prop('checked', true);

                    if (!filters.includes('modified')) {
                        filters.push('modified');
                    }
                }

                if (filters.length > 4) {
                    $('.filter-all').prop('checked', true);
                }
            }
        }

        autocomplete(searchInput, trs, filters);
        $('input[name="search"]').trigger('keyup');
        return false;
    });
});

(function () {
function get_selected(){
    let fileRows = $('.fileRow')
    let selectedIds = {}

    for (let row of fileRows){
        if (row.checked){
            if (Object.values(selectedIds).indexOf(row.getAttribute('id')) == -1){
                selectedIds.id = row.getAttribute('id')
            }
        }
    }
    let s = JSON.stringify(selectedIds)
    console.log(JSON.stringify(selectedIds))

    $.ajax({
        url: "/files/manage",
        type: 'POST',
        contentType: "application/json",
        data: JSON.stringify(s),   // converts js value to JSON string
        dataType: 'json',
        success: function(response) {
            console.log(response);
        }
    })
}

rows = document.querySelectorAll('.fileRow')
for (let i = 0; i < rows.length; i++){
    console.log('added')
    rows[i].addEventListener('click', get_selected)
}
})()
