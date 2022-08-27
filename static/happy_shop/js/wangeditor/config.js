var content = document.querySelector('#id_content')
var fieldContent = document.querySelectorAll('.field-content')
content.setAttribute('style', 'display:none')
fieldContent[0].querySelector('div').insertAdjacentHTML(
	'beforeend',
	'<div style="margin-left: 150px ;">\
    <div id="toolbar-container" style="border: solid 1px #eee;"></div>\
    <div id="editor-container" style="height:500px; border: solid 1px #eee; padding: 0 10px;"></div></div>'
)

// console.log(fieldContent[0].querySelector('div'))

const { createEditor, createToolbar } = window.wangEditor
// 编辑器配置
const editorConfig = { MENU_CONF: {} }
editorConfig.placeholder = '请输入内容'


editorConfig.MENU_CONF['uploadImage'] = {
	// 上传图片的配置
	server: '/upload_img/',
	// form-data fieldName ，默认值 'wangeditor-uploaded-image'
	fieldName: 'spuImg',

	// 单个文件的最大体积限制，默认为 2M
	maxFileSize: 5 * 1024 * 1024, // 1M

	// 最多可上传几个文件，默认为 100
	maxNumberOfFiles: 10,

	// 选择文件时的类型限制，默认为 ['image/*'] 。如不想限制，则设置为 []
	allowedFileTypes: ['image/*'],
}

editorConfig.onChange = (editor) => {
	// 当编辑器选区、内容变化时，即触发
	// console.log('content', editor.children)
	// console.log('html', editor.getHtml())
	content.value = editor.getHtml()
}

// 工具栏配置
const toolbarConfig = {}

// 创建编辑器
const editor = createEditor({
	selector: '#editor-container',
	config: editorConfig,
	mode: 'default', // 或 'simple' 参考下文
	html: content.value
})
//   创建工具栏
const toolbar = createToolbar({
	editor,
	selector: '#toolbar-container',
	config: toolbarConfig,
	mode: 'default' // 或 'simple' 参考下文
})