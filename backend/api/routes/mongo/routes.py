from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
import pymongo.errors

from .models import Book, BookUpdate
from .errors import ErrorCode
from .responses import (
    mongo_post_responses,
    mongo_get_responses,
    mongo_get_one_patch_delete_responses,
)


router = APIRouter()


@router.post("/", summary="Create a new book", description="Create a new book",
             response_description="The created book", status_code=status.HTTP_201_CREATED,
             response_model=Book, responses=mongo_post_responses)
async def create_book(request: Request, book: Book = Body(...)):
    book = jsonable_encoder(book)
    try:
        new_book = await request.app.database["books"].insert_one(book)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_EXISTS_ERROR,
                "reason": f"Book with ID {book.get('_id')} already exists"
            },
        )
    created_book = await request.app.database["books"].find_one(
        {"_id": new_book.inserted_id}
    )
    return created_book


@router.get("/", summary="Shows list of all books", description="Shows list of all books",
            response_description="List of all books", status_code=status.HTTP_200_OK,
            response_model=list[Book], responses=mongo_get_responses)
async def list_books(request: Request):
    books = [book async for book in request.app.database["books"].find(limit=100)]
    return books


@router.get("/{id_m}", summary="Shows the book by id", description="Shows the book by id",
            response_description="The single book", status_code=status.HTTP_200_OK,
            response_model=Book, responses=mongo_get_one_patch_delete_responses)
async def find_book(id_m: str, request: Request):
    if (book := await request.app.database["books"].find_one({"_id": id_m})) is not None:
        return book
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "code": ErrorCode.ID_NOT_FOUND,
            "reason": f"Book with ID {book.get('_id')} not found"
        },
    )


@router.patch("/{id_m}", summary="Update the book by id", description="Update the book by id",
              response_description="The single book", status_code=status.HTTP_200_OK,
              response_model=Book, responses=mongo_get_one_patch_delete_responses)
async def update_book(id_m: str, request: Request, book: BookUpdate = Body(...)):
    book = {k: v for k, v in book.dict().items() if v is not None}
    if len(book) >= 1:
        update_result = await request.app.database["books"].update_one(
            {"_id": id_m}, {"$set": book}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorCode.ID_NOT_FOUND,
                    "reason": f"Book with ID {id_m} not found"
                },
            )

    if (
        existing_book := await request.app.database["books"].find_one({"_id": id_m})
    ) is not None:
        return existing_book

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "code": ErrorCode.ID_NOT_FOUND,
            "reason": f"Book with ID {id_m} not found"
        },
    )


@router.delete("/{id_m}", summary="Delete the book by id", description="Delete the book by id",
               response_description="HTTP 200 STATUS", responses=mongo_get_one_patch_delete_responses)
async def delete_book(id_m: str, request: Request, response: Response):
    delete_result = await request.app.database["books"].delete_one({"_id": id_m})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "code": ErrorCode.ID_NOT_FOUND,
            "reason": f"Book with ID {id_m} not found"
        },
    )
