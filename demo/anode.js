
function Div( div, name, top, left )
{
	this.div = div;
	this.name = name;

	this.top = top;
	this.left = left;
	this.height = 0;
	this.width = 0;
}

function Entry( div )
{
	this.div = div;
}

Entry.prototype.output = function()
{
	var output = "&nbsp;&nbsp;&nbsp;&nbsp;.. annotation:: " 
					+ this.div.top + " "
					+ this.div.left + " "
					+ this.div.height + " "
					+ this.div.width;

	return output;
}

function State()
{
	this.image = "";
	this.entries = [];
	this.live = false;
}

State.prototype.new_div = function()
{
	return "new_div" + this.entries.length;
}

State.prototype.set_image = function( src )
{
	this.image = Image();
	this.image.src = src;
}

State.prototype.output = function()
{
	var output = ".. annotated-image:: " 
						+ this.image.height + " "
						+ this.image.width + " "
						+ this.image.src;

	for ( var i=0; i<this.entries.length; ++i )
	{
		output += "<br/>";
		output += this.entries[i].output();
	}

	return output;
}


state = new State();


function build_output()
{
	var output_text = state.output()

	var output = $("#output");

	output.html(output_text);
}


function image_mouse_down( info )
{
	var div_name = state.new_div();

	state.live = true;

	$("#imagebox").append("<div class='area' id='" + div_name + "'></div>");

	state.entries.push(
			new Entry(
				new Div(
					$("#" + div_name ),
					div_name,
					info.pageY - this.offsetTop,
					info.pageX - this.offsetLeft
					)
				)
			);

	var entry = state.entries[ state.entries.length - 1 ];
	var div = entry.div;

	div.div.css("position", "absolute");
	div.div.css("top", div.top + "px" );
	div.div.css("left", div.left + "px" );
}


function image_mouse_up( info )
{
	state.live = false;

	var entry = state.entries[ state.entries.length - 1 ];
	var div = entry.div;

	div.height = ( info.pageY - this.offsetTop ) - div.top;
	div.width = ( info.pageX - this.offsetLeft ) - div.left;

	if ( div.height < 1 || div.width < 1 )
	{
		state.entries.pop();
		div.remove();
		return;
	}

	div.div.css("position", "absolute");
	div.div.css("top", div.top + "px" );
	div.div.css("left", div.left + "px" );
	div.div.css("height", div.height + "px" );
	div.div.css("width", div.width + "px" );

	entry.name_id = "name_" + state.entries.length;
	entry.desc_id = "desc_" + state.entries.length;

	build_output();
}


function image_mouse_move( info )
{
	if ( ! state.live ) return;

	var entry = state.entries[ state.entries.length - 1 ];
	var div = entry.div;

	div.height = ( info.pageY - this.offsetTop ) - div.top;
	div.width = ( info.pageX - this.offsetLeft ) - div.left;

	div.div.css("height", div.height + "px" );
	div.div.css("width", div.width + "px" );
}


function image_key_callback( key ) 
{
	if ( key.which != 13 ) // Carriage return
		return;

	var imagesrc = $("#imagename").val();

	state.set_image( imagesrc );

	var height = state.image.height;
	var width = state.image.width;

	var imagebox = $("#imagebox");

	imagebox.css("position", "relative");
	imagebox.css("height", height + "px");
	imagebox.css("width", width + "px");
	imagebox.css("background-image", "url(" + imagesrc + ")");

	imagebox.mousedown( image_mouse_down );
	imagebox.mouseup( image_mouse_up );
	imagebox.mousemove( image_mouse_move );

}


function main()
{
	$("#imagename").keypress( image_key_callback );
}

