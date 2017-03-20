/// <reference path="../typings/index.d.ts" />
import * as angular from 'angular';

import 'angular-ui-router';
import 'angular-resource';
import 'angular-cookies';
import {xosVtrDashboardComponent} from './app/components/vtr/vtr-dashboard';
import {XosVtrTruckroll} from './app/services/truckroll.resource';

angular.module('xos-vtr-gui-extension', [
    'ui.router',
    'app'
  ])
  .service('XosVtrTruckroll', XosVtrTruckroll)
  .component('xosVtrDashboardComponent', xosVtrDashboardComponent)
  .run(function($log: ng.ILogService, XosNavigationService: any, XosRuntimeStates: any) {
    $log.info('[xos-vtr-gui-extension] App is running');

    XosNavigationService.add({
      label: 'Vtr',
      state: 'xos.vtr',
    });

    XosNavigationService.add({
      label: 'Dashboard',
      state: 'xos.vtr.dashboard',
      parent: 'xos.vtr'
    });

    XosRuntimeStates.addState(`xos.vtr`, {
      abstract: true,
      template: '<div ui-view></div>'
    });

    XosRuntimeStates.addState(`xos.vtr.dashboard`, {
      url: 'vtr/dashboard',
      parent: 'xos.vtr',
      component: 'xosVtrDashboardComponent'
    });
  });
