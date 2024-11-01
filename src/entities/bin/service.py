from datetime import timezone, datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
import uuid
from src.entities.bin.models import DustBin
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate


class DustBinService:
    @staticmethod
    async def get_all_dust_bins_page(
        session: AsyncSession,
    ) -> Page[DustBin]:
        """
        List all dust_bins
        """
        statement = select(DustBin)
        return await paginate(session, statement)

    @staticmethod
    async def create_dust_bin(
        session: AsyncSession,
        location: str,
    ) -> DustBin:
        """
        Create a new dust_bin
        """
        dust_bin = DustBin(
            id=uuid.uuid4(),
            location=location,
            created_at=datetime.now(timezone.utc),
        )

        session.add(dust_bin)
        await session.commit()
        await session.refresh(dust_bin)
        return dust_bin

    @staticmethod
    async def get_dust_bin_by_id(
        session: AsyncSession,
        id: uuid.UUID,
    ) -> DustBin | None:
        """
        Get a dust_bin by its id
        """
        statement = select(DustBin).where(DustBin.id == id)
        result = await session.exec(statement)
        return result.first()
