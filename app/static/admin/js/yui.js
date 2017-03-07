$(document).ready(function(){
    var config = {
            height: '420px',
            width: '900px',
            css: 'table td { border: 1px dashed #CCC } td { height: 15px; min-width:15px}',
            dompath: true, 
            animate: false,
            handleSubmit: true,
            toolbar: {
                collapse: true, 
                titlebar: 'Editor de Texto', 
                draggable: false, 
                buttonType: 'advanced', 
                buttons: [

                    { type: 'separator' },
                    { group: 'textstyle', label: 'Font Style',
                        buttons: [
                            { type: 'push', label: 'Bold CTRL + SHIFT + B', value: 'bold' },
                            { type: 'push', label: 'Italic CTRL + SHIFT + I', value: 'italic' },
                            { type: 'push', label: 'Underline CTRL + SHIFT + U', value: 'underline' },
                            { type: 'separator' },
                            { type: 'push', label: 'Subscript', value: 'subscript', disabled: true },
                            { type: 'push', label: 'Superscript', value: 'superscript', disabled: true }
                        ]
                    },
                    { type: 'separator' },
                    { group: 'textstyle2', label: '&nbsp;',
                        buttons: [
                            { type: 'color', label: 'Font Color', value: 'forecolor', disabled: true },
                            { type: 'color', label: 'Background Color', value: 'backcolor', disabled: true },
                            { type: 'separator' },
                            { type: 'push', label: 'Remove Formatting', value: 'removeformat', disabled: true },
                            { type: 'push', label: 'Show/Hide Hidden Elements', value: 'hiddenelements' }
                        ]
                    },
                    { type: 'separator' },
                    { group: 'undoredo', label: 'Undo/Redo',
                        buttons: [
                            { type: 'push', label: 'Undo', value: 'undo', disabled: true },
                            { type: 'push', label: 'Redo', value: 'redo', disabled: true }

                        ]
                    },
                    { type: 'separator' },
                    { group: 'alignment', label: 'Alignment',
                        buttons: [
                            { type: 'push', label: 'Align Left CTRL + SHIFT + [', value: 'justifyleft' },
                            { type: 'push', label: 'Align Center CTRL + SHIFT + |', value: 'justifycenter' },
                            { type: 'push', label: 'Align Right CTRL + SHIFT + ]', value: 'justifyright' },
                            { type: 'push', label: 'Justify', value: 'justifyfull' }
                        ]
                    },
                    { type: 'separator' },
                    { group: 'parastyle', label: 'Paragraph Style',
                        buttons: [
                        { type: 'select', label: 'Normal', value: 'heading', disabled: true,
                            menu: [
                                { text: 'Normal', value: 'none', checked: true },
                                { text: 'Header 1', value: 'h1' },
                                { text: 'Header 2', value: 'h2' },
                                { text: 'Header 3', value: 'h3' },
                                { text: 'Header 4', value: 'h4' },
                                { text: 'Header 5', value: 'h5' },
                                { text: 'Header 6', value: 'h6' }
                            ]
                        }
                        ]
                    },
                    { type: 'separator' },

                    { group: 'indentlist2', label: 'Indenting and Lists',
                        buttons: [
                            { type: 'push', label: 'Indent', value: 'indent', disabled: true },
                            { type: 'push', label: 'Outdent', value: 'outdent', disabled: true },
                            { type: 'push', label: 'Create an Unordered List', value: 'insertunorderedlist' },
                            { type: 'push', label: 'Create an Ordered List', value: 'insertorderedlist' }
                        ]
                    },
                    { type: 'separator' },
                    { group: 'insertitem', label: 'Insert Item',
                        buttons: [
                            { type: 'push', label: 'HTML Link CTRL + SHIFT + L', value: 'createlink', disabled: true },
                            { type: 'push', label: 'Insert Image', value: 'insertimage' },
                            { type: 'push', label: 'Insert Table', value: 'inserttable' }
                        ]
                    },
                    { type: 'separator'},
                    { group: 'html', label: 'HTML',
                        buttons: [
                            { type: 'push', label: 'Edit HTML Code', value: 'editcode' }
                        ]
                    }
                ]
            }
        },
        edit_html = function() {
            var state = 'off';
            this.toolbar.on('editcodeClick', function() {

                var ta = this.get('element'),
                    iframe = this.get('iframe').get('element');

                if (state == 'on') {
                    state = 'off';
                    this.toolbar.set('disabled', false);
                    YAHOO.log('Show the Editor', 'info', 'example');
                    YAHOO.log('Inject the HTML from the textarea into the editor', 'info', 'example');
                    this.setEditorHTML(ta.value);
                    if (!this.browser.ie) {
                        this._setDesignMode('on');
                    }

                    jQuery(iframe).removeClass('editor-hidden');
                    jQuery(ta).addClass('editor-hidden');
                    this.show();
                    this._focusWindow();
                } else {
                    state = 'on';
                    YAHOO.log('Show the Code Editor', 'info', 'example');
                    this.cleanHTML();
                    YAHOO.log('Save the Editors HTML', 'info', 'example');
                    jQuery(iframe).addClass('editor-hidden');
                    jQuery(ta).removeClass('editor-hidden');
                    this.toolbar.set('disabled', true);
                    this.toolbar.getButtonByValue('editcode').set('disabled', false);
                    this.toolbar.selectButton('editcode');
                    this.dompath.innerHTML = 'Editing HTML Code';
                    this.hide();
                }
                return false;
            }, this, true);

            this.on('cleanHTML', function(ev) {
                YAHOO.log('cleanHTML callback fired..', 'info', 'example');
                this.get('element').value = ev.html;
            }, this, true);

            this.on('afterRender', function() {
                var wrapper = this.get('editor_wrapper');
                wrapper.appendChild(this.get('element'));
                this.setStyle('width', '100%');
                this.setStyle('height', '100%');
                this.setStyle('visibility', '');
                this.setStyle('top', '');
                this.setStyle('left', '');
                this.setStyle('position', '');

                this.addClass('editor-hidden');

            }, this, true);
        };
    
    var editor = new YAHOO.widget.Editor('id_text', config);
    yuiImgUploader(editor, 'id_text', '/admin/image_upload/upload/','image');
    editor.initTableEditor();
    editor.on('toolbarLoaded',edit_html, editor, true);
    editor.render();
    
});