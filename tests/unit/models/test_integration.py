"""Cross-wrapper integration tests: factory methods return correct subclasses."""

from rhapsody_cli.models.core import AbstractRPModelElement, RPCollection, RPModelElement
from rhapsody_cli.models.elements.classifiers import RPClass, RPClassifier, RPStereotype
from rhapsody_cli.models.elements.common.model_misc import RPComment, RPConstraint, RPEnumerationLiteral
from rhapsody_cli.models.elements.containment import (
    RPComponent,
    RPConfiguration,
    RPPackage,
    RPProfile,
)
from rhapsody_cli.models.elements.relations import (
    RPAssociationRole,
    RPDependency,
    RPGeneralization,
    RPInstance,
)
from tests.unit.models.fakes import make_fake_collection, make_fake_element


def test_wrap_dispatches_profile_to_rpprofile() -> None:
    fake = make_fake_element("Profile", getName="SysML")

    result = AbstractRPModelElement.wrap(fake)

    assert isinstance(result, RPProfile)
    assert isinstance(result, RPPackage)


def test_wrap_dispatches_component_to_rpcomponent() -> None:
    fake = make_fake_element("Component", getName="Comp1")

    result = AbstractRPModelElement.wrap(fake)

    assert isinstance(result, RPComponent)


def test_wrap_dispatches_configuration_to_rpconfiguration() -> None:
    fake = make_fake_element("Configuration", getName="Config1")

    result = AbstractRPModelElement.wrap(fake)

    assert isinstance(result, RPConfiguration)


def test_wrap_dispatches_module_to_rpmodule() -> None:
    from rhapsody_cli.models.elements.containment import RPModule

    fake = make_fake_element("Module", getName="Module1")

    result = AbstractRPModelElement.wrap(fake)

    assert isinstance(result, RPModule)
    assert isinstance(result, RPInstance)


def test_wrap_dispatches_generalization_to_rpgeneralization() -> None:
    fake = make_fake_element("Generalization")

    result = AbstractRPModelElement.wrap(fake)

    assert isinstance(result, RPGeneralization)
    assert isinstance(result, RPModelElement)


def test_wrap_dispatches_dependency_to_rpdependency() -> None:
    fake = make_fake_element("Dependency")

    result = AbstractRPModelElement.wrap(fake)

    assert isinstance(result, RPDependency)
    assert isinstance(result, RPModelElement)


def test_wrap_dispatches_hyperlink_to_rphyperlink() -> None:
    from rhapsody_cli.models.elements.relations import RPHyperLink

    fake = make_fake_element("HyperLink")

    result = AbstractRPModelElement.wrap(fake)

    assert isinstance(result, RPHyperLink)
    assert isinstance(result, RPDependency)


def test_wrap_dispatches_association_role_to_rpassociation_role() -> None:
    fake = make_fake_element("AssociationRole")

    result = AbstractRPModelElement.wrap(fake)

    assert isinstance(result, RPAssociationRole)
    assert isinstance(result, RPInstance)


def test_wrap_dispatches_comment_to_rpcomment() -> None:
    fake = make_fake_element("Comment", getName="Comment1")

    result = AbstractRPModelElement.wrap(fake)

    assert isinstance(result, RPComment)
    assert isinstance(result, RPModelElement)


def test_wrap_dispatches_constraint_to_rpconstraint() -> None:
    fake = make_fake_element("Constraint", getName="Constraint1")

    result = AbstractRPModelElement.wrap(fake)

    assert isinstance(result, RPConstraint)
    assert isinstance(result, RPModelElement)


def test_wrap_dispatches_enumeration_literal_to_rpenumeration_literal() -> None:
    fake = make_fake_element("EnumerationLiteral", getName="LITERAL1")

    result = AbstractRPModelElement.wrap(fake)

    assert isinstance(result, RPEnumerationLiteral)
    assert isinstance(result, RPModelElement)


def test_wrap_dispatches_stereotype_to_rpstereotype() -> None:
    fake = make_fake_element("Stereotype", getName="MyStereo")

    result = AbstractRPModelElement.wrap(fake)

    assert isinstance(result, RPStereotype)
    assert isinstance(result, RPClassifier)


def test_wrap_dispatches_association_class_to_rpassociation_class() -> None:
    from rhapsody_cli.models.elements.classifiers import RPAssociationClass

    fake = make_fake_element("AssociationClass", getName="MyAssoc")

    result = AbstractRPModelElement.wrap(fake)

    assert isinstance(result, RPAssociationClass)
    assert isinstance(result, RPClass)


def test_wrap_dispatches_tag_to_rptag() -> None:
    from rhapsody_cli.models.elements.variables.model_variables import RPTag

    fake = make_fake_element("Tag", getName="MyTag")

    result = AbstractRPModelElement.wrap(fake)

    assert isinstance(result, RPTag)


def test_collection_contains_mixed_element_types() -> None:
    class1 = make_fake_element("Class", getName="Class1")
    actor1 = make_fake_element("Actor", getName="Actor1")
    coll = make_fake_collection([class1, actor1])

    result = RPCollection(coll)

    assert len(result) == 2
    assert isinstance(result[0], RPClass)
    assert isinstance(result[1], RPClassifier)


def test_all_new_wrappers_exist() -> None:
    """Verify all new wrappers can be imported."""
    from rhapsody_cli.models.elements.classifiers import (
        RPAssociationClass,
        RPStereotype,
    )
    from rhapsody_cli.models.elements.common.model_misc import (
        RPComment,
        RPConstraint,
        RPEnumerationLiteral,
    )
    from rhapsody_cli.models.elements.containment import (
        RPCollaboration,
        RPComponentInstance,
        RPModule,
        RPNode,
    )
    from rhapsody_cli.models.elements.relations import (
        RPAssociationRole,
        RPDependency,
        RPGeneralization,
        RPHyperLink,
    )
    from rhapsody_cli.models.elements.variables.model_variables import RPTag

    # All imports should succeed
    assert RPAssociationClass is not None
    assert RPStereotype is not None
    assert RPModule is not None
    assert RPNode is not None
    assert RPCollaboration is not None
    assert RPComponentInstance is not None
    assert RPGeneralization is not None
    assert RPDependency is not None
    assert RPHyperLink is not None
    assert RPAssociationRole is not None
    assert RPComment is not None
    assert RPConstraint is not None
    assert RPEnumerationLiteral is not None
    assert RPTag is not None
