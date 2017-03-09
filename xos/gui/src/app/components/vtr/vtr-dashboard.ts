import './vtr-dashboard.scss';
import * as _ from 'lodash';
import {subscribeOn} from 'rxjs/operator/subscribeOn';

class VtrDashboardComponent {
  static $inject = [
    '$timeout',
    'XosModelStore',
    'XosVtrTruckroll'
   ];

  public subscribers = [];
  public truckroll: any;
  public loader: boolean;
  public error: string;
  private Truckroll;

  constructor(
    private $timeout: ng.ITimeoutService,
    private XosModelStore: any,
    private XosVtrTruckroll: any
  ) {

    this.Truckroll = this.XosVtrTruckroll.getResource();

    // load subscribers
    this.XosModelStore.query('Subscribers')
      .subscribe(
        res => {
          this.subscribers = res;
        }
      );
  }

  public runTest() {

    // clean previous tests
    delete this.truckroll.id;
    delete this.truckroll.result;
    delete this.truckroll.is_synced;
    delete this.truckroll.result_code;
    delete this.truckroll.backend_status;
    delete this.error;

    this.truckroll.target_type_id = this.getSubscriberContentTypeId(this.truckroll.target_id);

    const test = new this.Truckroll(this.truckroll);
    this.loader = true;
    test.$save()
    .then((res) => {
      this.waitForTest(res.id);
    });
  };

  private getSubscriberContentTypeId(subscriberId: number) {
    return _.find(this.subscribers, {id: subscriberId}).self_content_type_id;
  }

  private waitForTest(id: number) {

        this.Truckroll.get({id: id}).$promise
        .then((testResult, status) => {
          // this is becasue error returning a string in an array
          if (testResult[0] && testResult[0].length === 1) {
            this.loader = false;
            this.error = 'An error occurred, please try again later';
            return;
          }

          // if error
          // or
          // if is synced
          if (
              testResult.backend_status.indexOf('2') >= 0 ||
              (testResult.result_code && testResult.result_code.indexOf('2') >= 0) ||
              testResult.is_synced
            ) {
            this.truckroll = angular.copy(testResult);
            this.loader = false;
            this.Truckroll.delete({id: id});
          }
          // else keep polling
          else {
            this.$timeout(() => {
              this.waitForTest(id);
            }, 2000);
          }
        });
      };

}

export const xosVtrDashboardComponent: angular.IComponentOptions = {
  template: require('./vtr-dashboard.html'),
  controllerAs: 'vm',
  controller: VtrDashboardComponent
};
