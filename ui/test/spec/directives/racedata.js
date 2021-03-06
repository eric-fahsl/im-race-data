'use strict';

describe('Directive: raceData', function () {

  // load the directive's module
  beforeEach(module('uiApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<race-data></race-data>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the raceData directive');
  }));
});
