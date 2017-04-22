
'use strict';

var myApp=angular.module('myApp',['ngRoute',]);

// routing configuration
myApp.config(['$routeProvider',
function($routeProvider){
$routeProvider.when('/',{
	templateUrl:'/static/partials/index.html'
}).when('/about',{
	templateUrl:'/static/partials/about.html'
}).when('/register',{
	templateUrl:'/static/partials/register.html'
}).when('/login',{
	templateUrl:'/static/partials/login.html'
}).when('/task',{
	templateUrl:'static/partials/task.html'
}).otherwise(
{
	redirectTo:'/'
});

}]);

