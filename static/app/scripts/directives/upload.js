angular.module('staticApp')
  .directive('ngFileUpload', function ($log) {
    return {
      transclude: true,
      link: function(scope, element) {
        $log.debug('Loading file upload');

		element.fileupload({
			dataType: 'json',
			done: function (e, data) {
				scope.uploading = false;
				scope.loading = true;
				$log.debug(data.result);
				scope.imageName = data.result.name;
				$log.debug('Uploaded ' + scope.imageName);
				scope._markers = data.result.markers;
				scope.$apply();

			},
			start: function () {
				scope.markers = [];
				scope.uploading = true;
				scope.$apply();
				return true;
			}
		});
      }
    }
});