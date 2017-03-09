export default routesConfig;

function routesConfig($stateProvider: angular.ui.IStateProvider, $locationProvider: angular.ILocationProvider) {
  $locationProvider.html5Mode(false).hashPrefix('');

  $stateProvider
  .state('xos.vtr', {
      abstract: true,
      template: '<div ui-view></div>'
    })
    .state('xos.vtr.dashboard', {
      url: 'vtr/dashboard',
      parent: 'xos.vtr',
      component: 'xosVtrDashboardComponent'
    });
}
