'use strict';

/**
 * @ngdoc overview
 * @name staticApp
 * @description
 * # staticApp
 *
 * Main module of the application.
 */
angular
  .module('staticApp', [
    'ngAnimate',
    'ngCookies',
    'ngSanitize',
    'ngTouch',
    'ngRoute'
  ]).config (function ($routeProvider) {
  $routeProvider.when(
    '/', {
      templateUrl: 'views/main-en.html',
      controller: 'DemoCtrl'
    }
  ).when(
      '/en', {
        templateUrl: 'views/main-en.html',
        controller: 'DemoCtrl'
      }
  ).when(
      '/ru', {
        templateUrl: 'views/main-ru.html',
        controller: 'DemoCtrl'
      }
  )
  .otherwise({
    redirectTo: '/'
  });
});
