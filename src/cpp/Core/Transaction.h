/***************************************************************************
 *   Copyright (c) 2011 Jürgen Riegel <juergen.riegel@web.de>              *
 *   Copyright (c) 2011 Werner Mayer <wmayer[at]users.sourceforge.net>     *
 *                                                                         *
 *   This file is part of the FreeCAD CAx development system.              *
 *                                                                         *
 *   This library is free software; you can redistribute it and/or         *
 *   modify it under the terms of the GNU Library General Public           *
 *   License as published by the Free Software Foundation; either          *
 *   version 2 of the License, or (at your option) any later version.      *
 *                                                                         *
 *   This library  is distributed in the hope that it will be useful,      *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU Library General Public License for more details.                  *
 *                                                                         *
 *   You should have received a copy of the GNU Library General Public     *
 *   License along with this library; see the file COPYING.LIB. If not,    *
 *   write to the Free Software Foundation, Inc., 59 Temple Place,         *
 *   Suite 330, Boston, MA  02111-1307, USA                                *
 *                                                                         *
 ***************************************************************************/


#pragma once

#include <Base/Factory.h>
#include <Base/Persistence.h>
#include <Core/DynamicProperty.h>
#include <unordered_map>


namespace Core
{

class CoreDocument;
class Property;
class DocObject;
class TransactionP;

/** Represents a atomic transaction of the document
 */
class LX_CORE_EXPORT Transaction : public Base::Persistence
{
    TYPESYSTEM_HEADER();

public:
    /** Construction
     *
     * @param id: transaction id. If zero, then it will be generated
     * automatically as a monotonically increasing index across the entire
     * application. User can pass in a transaction id to group multiple
     * transactions from different document, so that they can be undo/redo
     * together.
     */
    Transaction(int id = 0);
    /// Construction
    virtual ~Transaction();

    /// apply the content to the document
    void apply(CoreDocument &Doc,bool forward);

    // the utf-8 name of the transaction
    std::string Name;

    virtual void save(Base::AbstractWriter& /*writer*/, Base::PersistenceVersion& /*save_version*/);
    /// This method is used to restore properties from an XML document.
    virtual void restore(Base::AbstractXMLReader& /*reader*/, Base::PersistenceVersion& /*version*/);

    /// Return the transaction ID
    int getID(void) const;

    /// Generate a new unique transaction ID
    static int getNewID(void);
    static int getLastID(void);

    /// Returns true if the transaction list is empty; otherwise returns false.
    bool isEmpty() const;
    /// check if this object is used in a transaction
    bool hasObject(const Core::DocObject *Obj) const;
    void addOrRemoveProperty(Core::DocObject *Obj, const Property* pcProp, bool add);

    void addObjectNew(Core::DocObject *Obj);
    void addObjectDel(const Core::DocObject *Obj);
    void addObjectChange(const Core::DocObject *Obj, const Property *Prop);

private:
    int transID;
    std::unique_ptr<TransactionP> mPimpl;
};

/** Represents an entry for an object in a Transaction
 */
class LX_CORE_EXPORT TransactionObject : public Base::Persistence
{
    TYPESYSTEM_HEADER();

public:
    /// Construction
    TransactionObject();
    /// Destruction
    virtual ~TransactionObject();

    virtual void applyNew(CoreDocument &Doc, Core::DocObject *pcObj);
    virtual void applyDel(CoreDocument &Doc, Core::DocObject *pcObj);
    virtual void applyChn(CoreDocument &Doc, Core::DocObject *pcObj, bool Forward);

    void setProperty(const Property* pcProp);
    void addOrRemoveProperty(const Property* pcProp, bool add);

    virtual void save(Base::AbstractWriter& /*writer*/, Base::PersistenceVersion& /*save_version*/);
    /// This method is used to restore properties from an XML document.
    virtual void restore(Base::AbstractXMLReader& /*reader*/, Base::PersistenceVersion& /*version*/);

    friend class Transaction;

protected:
    enum Status {New,Del,Chn} status;

#ifndef SWIG
    struct PropData : DynamicProperty::PropData {
        Base::Type propertyType;
    };
    std::unordered_map<const Property*, PropData> _PropChangeMap;
#endif
    std::string _NameInDocument;
};

/** Represents an entry for a document object in a transaction
 */
class LX_CORE_EXPORT TransactionDocumentObject : public TransactionObject
{
    TYPESYSTEM_HEADER();

public:
    /// Construction
    TransactionDocumentObject();
    /// Destruction
    virtual ~TransactionDocumentObject();

    void applyNew(CoreDocument &Doc, Core::DocObject *pcObj);
    void applyDel(CoreDocument &Doc, Core::DocObject *pcObj);
};

class LX_CORE_EXPORT TransactionFactory
{
public:
    static TransactionFactory& instance();
    static void destruct ();

    TransactionObject* createTransaction (const Base::Type& type) const;
    void addProducer (const Base::Type& type, Base::AbstractProducer *producer);

private:
    static TransactionFactory* self;
    std::map<Base::Type, Base::AbstractProducer*> producers;

    TransactionFactory(){}
    ~TransactionFactory(){}
};

template <class CLASS>
class TransactionProducer : public Base::AbstractProducer
{
public:
    TransactionProducer (const Base::Type& type)
    {
        TransactionFactory::instance().addProducer(type, this);
    }

    virtual ~TransactionProducer (){}

    /**
     * Creates an instance of the specified transaction object.
     */
    virtual void* Produce () const
    {
        return (new CLASS);
    }
};

} //namespace Core


