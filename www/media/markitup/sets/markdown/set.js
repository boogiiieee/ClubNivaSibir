// -------------------------------------------------------------------
// markItUp!
// -------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// -------------------------------------------------------------------
// MarkDown tags example
// http://en.wikipedia.org/wiki/Markdown
// http://daringfireball.net/projects/markdown/
// -------------------------------------------------------------------
// Feel free to add more tags
// -------------------------------------------------------------------
mySettings = {
	onShiftEnter:		{keepDefault:false, openWith:'\n'},
	markupSet: [
		{name:'Заголовок 1го уровня', key:'1', placeHolder:'Ваш заголовок...', closeWith:function(markItUp) { return miu.markdownTitle(markItUp, '=') } },
		{name:'Заголовок 2го уровня', key:'2', placeHolder:'Ваш заголовок...', closeWith:function(markItUp) { return miu.markdownTitle(markItUp, '-') } },
		{name:'Заголовок 3го уровня', key:'3', openWith:'### ', placeHolder:'Ваш заголовок...' },
		{name:'Заголовок 4го уровня', key:'4', openWith:'#### ', placeHolder:'Ваш заголовок...' },
		{name:'Заголовок 5го уровня', key:'5', openWith:'##### ', placeHolder:'Ваш заголовок...' },
		{name:'Заголовок 6го уровня', key:'6', openWith:'###### ', placeHolder:'Ваш заголовок...' },
		{separator:'---------------' },		
		{name:'Жирный', key:'B', openWith:'**', closeWith:'**'},
		{name:'Курсив', key:'I', openWith:'_', closeWith:'_'},
		{separator:'---------------' },
		{name:'Список', openWith:'- ' },
		{name:'Нумерованный список', openWith:function(markItUp) {
			return markItUp.line+'. ';
		}},
		{separator:'---------------' },
		{name:'Изображение', key:'P', replaceWith:'![[![Альтернативный текст]!]]([![Ссылка:!:http://]!] "[![Заголовок]!]")'},
		{name:'Видео', key:'V', replaceWith:'|video|([![YouTube:!:http://]!])', className:"video"},
		{name:'Ссылка', key:'L', openWith:'[', closeWith:']([![Ссылка:!:http://]!] "[![Заголовок]!]")', placeHolder:'Текст ссылки...' },
		{separator:'---------------'},	
	]
}

// mIu nameSpace to avoid conflict.
miu = {
	markdownTitle: function(markItUp, char) {
		heading = '';
		n = $.trim(markItUp.selection||markItUp.placeHolder).length;
		// work around bug in python-markdown where header underlines must be at least 3 chars
		if (n < 3) { n = 3; }
		for(i = 0; i < n; i++) {
			heading += char;
		}
		return '\n'+heading;
	}
}
