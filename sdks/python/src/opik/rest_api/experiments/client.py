# This file was auto-generated by Fern from our API Definition.

import typing
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.jsonable_encoder import jsonable_encoder
from ..core.pydantic_utilities import pydantic_v1
from ..core.request_options import RequestOptions
from ..errors.not_found_error import NotFoundError
from ..types.experiment_item import ExperimentItem
from ..types.experiment_item_public import ExperimentItemPublic
from ..types.experiment_page_public import ExperimentPagePublic
from ..types.experiment_public import ExperimentPublic
from ..types.json_node_write import JsonNodeWrite

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class ExperimentsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def find_experiments(
        self,
        *,
        page: typing.Optional[int] = None,
        size: typing.Optional[int] = None,
        dataset_id: typing.Optional[str] = None,
        name: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ExperimentPagePublic:
        """
        Find experiments

        Parameters
        ----------
        page : typing.Optional[int]

        size : typing.Optional[int]

        dataset_id : typing.Optional[str]

        name : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExperimentPagePublic
            Experiments resource

        Examples
        --------
        from Opik.client import OpikApi

        client = OpikApi()
        client.experiments.find_experiments()
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/private/experiments",
            method="GET",
            params={"page": page, "size": size, "datasetId": dataset_id, "name": name},
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(ExperimentPagePublic, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create_experiment(
        self,
        *,
        dataset_name: str,
        name: str,
        id: typing.Optional[str] = OMIT,
        metadata: typing.Optional[JsonNodeWrite] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Create experiment

        Parameters
        ----------
        dataset_name : str

        name : str

        id : typing.Optional[str]

        metadata : typing.Optional[JsonNodeWrite]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from Opik.client import OpikApi

        client = OpikApi()
        client.experiments.create_experiment(
            dataset_name="dataset_name",
            name="name",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/private/experiments",
            method="POST",
            json={
                "id": id,
                "dataset_name": dataset_name,
                "name": name,
                "metadata": metadata,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create_experiment_items(
        self,
        *,
        experiment_items: typing.Sequence[ExperimentItem],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Create experiment items

        Parameters
        ----------
        experiment_items : typing.Sequence[ExperimentItem]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from Opik import ExperimentItem
        from Opik.client import OpikApi

        client = OpikApi()
        client.experiments.create_experiment_items(
            experiment_items=[
                ExperimentItem(
                    experiment_id="experiment_id",
                    dataset_item_id="dataset_item_id",
                    trace_id="trace_id",
                )
            ],
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/private/experiments/items",
            method="POST",
            json={"experiment_items": experiment_items},
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete_experiment_items(
        self,
        *,
        ids: typing.Sequence[str],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Delete experiment items

        Parameters
        ----------
        ids : typing.Sequence[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from Opik.client import OpikApi

        client = OpikApi()
        client.experiments.delete_experiment_items(
            ids=["ids"],
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/private/experiments/items/delete",
            method="POST",
            json={"ids": ids},
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_experiment_by_id(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> ExperimentPublic:
        """
        Get experiment by id

        Parameters
        ----------
        id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExperimentPublic
            Experiment resource

        Examples
        --------
        from Opik.client import OpikApi

        client = OpikApi()
        client.experiments.get_experiment_by_id(
            id="id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/private/experiments/{jsonable_encoder(id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(ExperimentPublic, _response.json())  # type: ignore
            if _response.status_code == 404:
                raise NotFoundError(
                    pydantic_v1.parse_obj_as(typing.Any, _response.json())
                )  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_experiment_item_by_id(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> ExperimentItemPublic:
        """
        Get experiment item by id

        Parameters
        ----------
        id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExperimentItemPublic
            Experiment item resource

        Examples
        --------
        from Opik.client import OpikApi

        client = OpikApi()
        client.experiments.get_experiment_item_by_id(
            id="id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/private/experiments/items/{jsonable_encoder(id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(ExperimentItemPublic, _response.json())  # type: ignore
            if _response.status_code == 404:
                raise NotFoundError(
                    pydantic_v1.parse_obj_as(typing.Any, _response.json())
                )  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncExperimentsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def find_experiments(
        self,
        *,
        page: typing.Optional[int] = None,
        size: typing.Optional[int] = None,
        dataset_id: typing.Optional[str] = None,
        name: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ExperimentPagePublic:
        """
        Find experiments

        Parameters
        ----------
        page : typing.Optional[int]

        size : typing.Optional[int]

        dataset_id : typing.Optional[str]

        name : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExperimentPagePublic
            Experiments resource

        Examples
        --------
        import asyncio

        from Opik.client import AsyncOpikApi

        client = AsyncOpikApi()


        async def main() -> None:
            await client.experiments.find_experiments()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/private/experiments",
            method="GET",
            params={"page": page, "size": size, "datasetId": dataset_id, "name": name},
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(ExperimentPagePublic, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def create_experiment(
        self,
        *,
        dataset_name: str,
        name: str,
        id: typing.Optional[str] = OMIT,
        metadata: typing.Optional[JsonNodeWrite] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Create experiment

        Parameters
        ----------
        dataset_name : str

        name : str

        id : typing.Optional[str]

        metadata : typing.Optional[JsonNodeWrite]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        import asyncio

        from Opik.client import AsyncOpikApi

        client = AsyncOpikApi()


        async def main() -> None:
            await client.experiments.create_experiment(
                dataset_name="dataset_name",
                name="name",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/private/experiments",
            method="POST",
            json={
                "id": id,
                "dataset_name": dataset_name,
                "name": name,
                "metadata": metadata,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def create_experiment_items(
        self,
        *,
        experiment_items: typing.Sequence[ExperimentItem],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Create experiment items

        Parameters
        ----------
        experiment_items : typing.Sequence[ExperimentItem]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        import asyncio

        from Opik import ExperimentItem
        from Opik.client import AsyncOpikApi

        client = AsyncOpikApi()


        async def main() -> None:
            await client.experiments.create_experiment_items(
                experiment_items=[
                    ExperimentItem(
                        experiment_id="experiment_id",
                        dataset_item_id="dataset_item_id",
                        trace_id="trace_id",
                    )
                ],
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/private/experiments/items",
            method="POST",
            json={"experiment_items": experiment_items},
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def delete_experiment_items(
        self,
        *,
        ids: typing.Sequence[str],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Delete experiment items

        Parameters
        ----------
        ids : typing.Sequence[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        import asyncio

        from Opik.client import AsyncOpikApi

        client = AsyncOpikApi()


        async def main() -> None:
            await client.experiments.delete_experiment_items(
                ids=["ids"],
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/private/experiments/items/delete",
            method="POST",
            json={"ids": ids},
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_experiment_by_id(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> ExperimentPublic:
        """
        Get experiment by id

        Parameters
        ----------
        id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExperimentPublic
            Experiment resource

        Examples
        --------
        import asyncio

        from Opik.client import AsyncOpikApi

        client = AsyncOpikApi()


        async def main() -> None:
            await client.experiments.get_experiment_by_id(
                id="id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/private/experiments/{jsonable_encoder(id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(ExperimentPublic, _response.json())  # type: ignore
            if _response.status_code == 404:
                raise NotFoundError(
                    pydantic_v1.parse_obj_as(typing.Any, _response.json())
                )  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_experiment_item_by_id(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> ExperimentItemPublic:
        """
        Get experiment item by id

        Parameters
        ----------
        id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExperimentItemPublic
            Experiment item resource

        Examples
        --------
        import asyncio

        from Opik.client import AsyncOpikApi

        client = AsyncOpikApi()


        async def main() -> None:
            await client.experiments.get_experiment_item_by_id(
                id="id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/private/experiments/items/{jsonable_encoder(id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(ExperimentItemPublic, _response.json())  # type: ignore
            if _response.status_code == 404:
                raise NotFoundError(
                    pydantic_v1.parse_obj_as(typing.Any, _response.json())
                )  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
