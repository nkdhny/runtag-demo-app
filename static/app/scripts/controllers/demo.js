'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:DemoCtrl
 * @description
 * # DemoCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('DemoCtrl', function ($scope, $log, $timeout) {
    $scope.markers = [];
    $scope.init = function() {




		angular.element('.result-image').on('load', function () {
			$log.debug('Image loaded');
			$timeout(function () {
				drawImage($scope._markers);
			}, 300);
			$scope.loading = false;
			$scope.$apply();
		});

    };

    $scope.upload = function($event) {
    	$event.preventDefault();
    	angular.element('input').click();
    };

    var drawImage = function(markers) {
    	angular.element('.marker').remove();
    	var $container = angular.element('.result-holder');
    	var $image = $container.find('img');
    	var width = $image.width();
    	var height = $image.height();

    	$log.debug(width, height);

    	for (var i = markers.length - 1; i >= 0; i--) {
    		var m = markers[i];
    		$scope.markers.push(m.id);
    		var $m = angular.element('<DIV></DIV>').addClass('marker').css({
    			left: m.left*width+'px',
    			top: m.top*height+'px',
    			width: m.width*width+'px',
    			height: m.height*height+'px',
    		});

    		$container.append($m);
    	}
    };
  });
