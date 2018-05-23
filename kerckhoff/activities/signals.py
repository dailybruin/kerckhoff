import django.dispatch

package_updated = django.dispatch.Signal(providing_args=["user, package"])
package_created = django.dispatch.Signal(providing_args=["user, pacakge"])
