
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

function State()
{
	this.entries = []
}

State.prototype.new_div = function()
{
	return "new_div" + this.entries.length;
}

state = new State();

function image_mouse_down( info )
{
	var div_name = state.new_div();

	$("#imagebox").append("<div class='area' id='" + div_name + "'></div>");

	state.entries.push( new Entry( new Div( $("#" + div_name ), div_name, info.pageY - this.offsetTop, info.pageX - this.offsetLeft ) ) );

	// $("#entries").html( info.pageX + " " + info.pageY + " <br/>" + this.offsetLeft + " " + this.offsetTop + "<br/>Id: " + div_name );
}

function image_mouse_up( info )
{
	var entry = state.entries[ state.entries.length - 1 ];
	var div = entry.div;

	div.height = ( info.pageY ) - div.top;
	div.width = ( info.pageX ) - div.left;

	if ( div.height < 1 || div.width < 1 )
	{
		state.entries.pop();
		div.remove();
		return;
	}

	// $("#output").html( div.top + " " + div.left + "<br/> " + div.height + " " + div.width + " <br/> " + this.offsetTop + " " + this.offsetLeft + "<br/>Length: " + state.divs.length + "<br/>Id: " +  div.name );

	div.div.css("top", div.top + "px" );
	div.div.css("left", div.left + "px" );
	div.div.css("height", div.height + "px" );
	div.div.css("width", div.width + "px" );
	div.div.css("position", "absolute");

	var form = $("#entries form");

	form
		.append("<div>")
		.append("Name: <input type='text'/>")
	    .append("Description: <textarea></textarea>")
	    .append("</div>");
}

function image_mouse_move( info )
{
}





function image_key_callback( key ) 
{
	if ( key.which != 13 ) // Carriage return
		return;

	var imagesrc = $("#imagename").val();

	var image = Image();
	image.src = imagesrc;

	var height = image.height;
	var width = image.width;

	var imagebox = $("#imagebox");

	imagebox.css("position", "relative");
	imagebox.css("height", height + "px");
	imagebox.css("width", width + "px");
	imagebox.css("background-image", "url(" + imagesrc + ")");

	imagebox.mousedown( image_mouse_down );
	imagebox.mouseup( image_mouse_up );
	// imagebox.mousemove( image_mouse_move );

}

function main()
{
	$("#imagename").keypress( image_key_callback );
}

