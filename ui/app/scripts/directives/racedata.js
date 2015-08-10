'use strict';

/**
 * @ngdoc directive
 * @name uiApp.directive:raceData
 * @description
 * # raceData
 */
angular.module('uiApp')
  .directive('raceData', function () {
    return {
      restrict: 'E',
      templateUrl: 'views/racedata.html',
      controller: function($scope, $rootScope, dataService) {
          // if (!$rootScope.summaryData) {
          //   $rootScope.summaryData = {};
          // }

          // $rootScope.summaryData[$scope.bib] = $scope.bib;

          $scope.highlighted = 'highlighted';
          $scope.refreshData = function() {
            $scope.loadingstatus = 'loading';
            dataService.getRaceResults($scope.raceid, $scope.racename, $scope.bib, $scope.starttime).then(
              function(data) {
                $scope.data = data;
                // $rootScope.summaryData[data.bib] = 'data.lastNextSplit';
                // $rootScope.summaryData[data.bib] = data.bib;
                
                $scope.loadingstatus = '';
                
                console.log('before data switch');

                var latestUpdate = {
                  bib: data.bib,
                  name: data.name, 
                  currentSport: data.lastNextSplit.sport,
                  lastCheckPointLoc: data.lastNextSplit.previous.totalDistance, 
                  lastCheckPointRaceTime: data.lastNextSplit.previous.raceTime, 
                  nextCheckPointLoc: data.lastNextSplit.next.totalDistance, 
                  nextCheckPointRaceTime: data.lastNextSplit.previous.estimatedRaceTime
                };

                // $rootScope.tableData = [{name: 'Tiancum', age: 43},
                //     {name: 'Jacob', age: 27},
                //     {name: 'Nephi', age: 29},
                //     {name: 'Enos', age: 34},
                //     {name: 'Tiancum', age: 43},
                //     {name: 'Jacob', age: 27},
                //     {name: 'Nephi', age: 29},
                //     {name: 'Enos', age: 34},
                //     {name: 'Tiancum', age: 43},
                //     {name: 'Jacob', age: 27},
                //     {name: 'Nephi', age: 29},
                //     {name: 'Enos', age: 34},
                //     {name: 'Tiancum', age: 43},
                //     {name: 'Jacob', age: 27},
                //     {name: 'Nephi', age: 29},
                //     {name: 'Enos', age: 34}];

                $rootScope.updateTableParams(latestUpdate);

                console.log(data);

              }
            );

          };

          $scope.refreshData();
          // console.log($rootScope.summaryData);

      },
      scope: {
      	raceid: '@',
        racename: '@',
        starttime: '@',
        bib: '='
      }
    };
  });
