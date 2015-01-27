
var I_Starter = 
{
	create : function(){},
	populate : function(){},
	start : function(){}
};

function Starter ()
{
	this.baseGUI;
	this.baseMap;
}

Starter.prototype.constructor = function() 
{
	Starter.superClass.call(this);
};
     		
Starter.prototype.create = function()
{
	this.baseGUI.createGUI(this.parent_element, this.baseMap);
};


Starter.prototype.populate = function(json_query)
{	
	this.baseMap.base_log();
	this.baseMap.getMap(json_query);
};

// Starter.prototype.populate = function()
// {
	// Object.abstract();
// };


Starter.prototype.start = function(parent_element, baseGUI, baseMap)
{
	this.starter = this;
	this.parent_element = parent_element;
	this.baseGUI = new baseGUI(this.parent_element);

//    console.log( 'this.baseGUI: : ', this.baseGUI)

	this.baseMap = new baseMap(this.baseGUI.populateGUI, this.baseGUI.updateGUI);
	
	this.create();
	this.populate();

};

Starter.implement(I_Starter);


