/// <reference path="../typings/index.d.ts" />
import * as angular from 'angular';

import 'angular-ui-router';
import 'angular-resource';
import 'angular-cookies';
import routesConfig from './routes';
import {xosVtrDashboardComponent} from './app/components/vtr/vtr-dashboard';
import {XosVtrTruckroll} from './app/services/truckroll.resource';

angular.module('xos-vtr-gui-extension', [
    'ui.router',
    'app'
  ])
  .config(routesConfig)
  .service('XosVtrTruckroll', XosVtrTruckroll)
  .component('xosVtrDashboardComponent', xosVtrDashboardComponent)
  .run(function($log: ng.ILogService, XosNavigationService: any) {
    $log.info('[xos-vtr-gui-extension] App is running');

    XosNavigationService.add({
      label: 'vTR',
      state: 'xos.vtr',
    });

    XosNavigationService.add({
      label: 'Dashboard',
      state: 'xos.vtr.dashboard',
      parent: 'xos.vtr'
    });
  });
