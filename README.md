# Virtual Truckroll Service

The `vTR` service is designed to perform a connectivity test in place of the subscriber. It will save you time and costs of sending a truck to the subscriber premises to perform the same kind of test.

## Onboarding

To onboard this service in your system, you can execute the `onboard-vtr.yaml` playbook, using this command:

```
ansible-playbook -i /etc/maas/ansible/pod-inventory --extra-vars=@/opt/cord/build/genconfig/config.yml onboard-vtr-playbook.yaml
```
