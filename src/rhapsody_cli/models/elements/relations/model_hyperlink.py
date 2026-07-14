"""Wraps ``com.telelogic.rhapsody.core.IRPHyperLink``."""

from typing import TYPE_CHECKING

from rhapsody_cli.models.core import AbstractRPModelElement, RPModelElement
from rhapsody_cli.models.elements.relations.model_dependency import RPDependency

if TYPE_CHECKING:
    pass


class RPHyperLink(RPDependency):
    """Wraps ``IRPHyperLink``: a hyperlink that extends ``IRPDependency``."""

    # IRPHyperLink method parity checklist:
    # [deprecated] getTextToDisplay  - skipped (deprecated in Rhapsody Java API; see deprecated-list.html)
    # [deprecated] getTextToDisplayType  - skipped (deprecated in Rhapsody Java API; see deprecated-list.html)
    # [deprecated] getDisplayOption  - skipped (deprecated in Rhapsody Java API; see deprecated-list.html)
    # [x] getTarget  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] getURL  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] setDisplayOption  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] setTarget  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [x] setURL  [x] impl  [x] docstring  [ ] unit test  [ ] integration test
    # [inherited] IRPDependency / IRPModelElement methods (covered by RPDependency / RPModelElement checklists)
    # Deprecated IRPHyperLink methods listed above.

    def get_target(self) -> RPModelElement:
        """Returns the target element of the hyperlink.

        Returns:
            The wrapped target model element.

        Reference:
            com.telelogic.rhapsody.core.IRPHyperLink::getTarget()
        """
        return AbstractRPModelElement.wrap(AbstractRPModelElement._get_method_or_property(self._com, "getTarget", "target"))

    def get_url(self) -> str:
        """Returns the URL of the hyperlink.

        Returns:
            The URL string.

        Reference:
            com.telelogic.rhapsody.core.IRPHyperLink::getURL()
        """
        return str(AbstractRPModelElement._get_method_or_property(self._com, "getURL", "url"))

    def set_display_option(self, display_option: int) -> None:
        """Sets the display option for the hyperlink.

        Args:
            display_option: The display option value.

        Reference:
            com.telelogic.rhapsody.core.IRPHyperLink::setDisplayOption(int displayOption)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setDisplayOption(display_option))

    def set_target(self, target: RPModelElement) -> None:
        """Sets the target element of the hyperlink.

        Args:
            target: The wrapped target model element.

        Reference:
            com.telelogic.rhapsody.core.IRPHyperLink::setTarget(com.telelogic.rhapsody.core.IRPModelElement target)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setTarget(target._com))

    def set_url(self, url: str) -> None:
        """Sets the URL of the hyperlink.

        Args:
            url: The URL string to set.

        Reference:
            com.telelogic.rhapsody.core.IRPHyperLink::setURL(java.lang.String url)
        """
        AbstractRPModelElement.call_com(lambda: self._com.setURL(url))


AbstractRPModelElement.register_wrapper("HyperLink", RPHyperLink)
