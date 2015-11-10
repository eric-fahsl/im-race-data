'use strict';

/**
 * @ngdoc service
 * @name uiApp.dataService
 * @description
 * # dataService
 * Service in the uiApp.
 */
angular.module('uiApp')
  .service('dataService', function ($http, $q) {
    // AngularJS will instantiate a singleton by calling "new" on this function
    var factory = {};

	factory.getRaceResults = function(raceId, raceName, bib, startTime) {
		// whereshouldiski.com/im/api.php?raceId=2147483665&raceName=neworleans70.3&bib=2
		var deferred = $q.defer();
		$http({
			// url: 'http://54.245.232.47/im/api-new.php',
			// url: 'http://localhost:8000',
			url: 'https://im-scraper-api.herokuapp.com',
			method: 'GET',
			params: {
				r: Math.random(),
				raceId: raceId,
				raceName: raceName,
				bib: bib,
				startTime: startTime
			}
		}).success(function(data) {
			if (data) {
				deferred.resolve(data);	
			}
			else {
				deferred.reject();
			}
		}).error(function() {
			console.error('Error retrieving data from search.');
			deferred.reject();
		});
		return deferred.promise;
	};

	return factory;
  });


